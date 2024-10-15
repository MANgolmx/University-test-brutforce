from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta
import os
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import random
import time
import json
import re

# URL of the login page and the target page
login_url = 'https://phys-online.ru/login/index.php'
target_url = 'https://phys-online.ru/mod/quiz/view.php?id=60'

# Your login credentials
username = ''
password = ''

# Path to your 
driver_path = 'C:\\Users\\misam\\OneDrive\\Документы\\chromedriver-win64\\chromedriver.exe'  # Update with the correct path

pageCount = 4 # Update with number of pages

sleepTime = 300

def convert_to_database_format(data):
    new_data = []
    
    for item in data:
        new_item = {
            "name": item["name"],
            "solved": item["solved"],
            "answer_right": item["answer"] if item["solved"] else None,
            "answer_wrong": [] if item["solved"] else [item["answer"]]
        }
        new_data.append(new_item)
    
    return new_data

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def clean_text(text):
    if text == None:
        return ""
    return text.replace(' ', '').replace('\n', '')

def push_to_database(filename, datalist):
    """
    Pushes datalist to database. If an entry with the same name exists, it updates the existing entry.
    Otherwise, it adds a new entry.
    """
    # Load existing data from the database file
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            database = json.load(file)
    else:
        database = []

    # Clean and update the datalist
    for data in datalist:
        data['name'] = clean_text(data['name'])
        data['answer_right'] = clean_text(data['answer_right'])
        data['answer_wrong'] = [clean_text(wrong) for wrong in data['answer_wrong']]
        
        # Check if the data with this name already exists in the database
        found = False
        for entry in database:
            if entry['name'] == data['name']:
                entry['solved'] = data['solved']
                entry['answer_right'] = data['answer_right']
                if data['answer_right']:
                    entry['answer_wrong'] = [""]
                else:
                    entry['answer_wrong'] = list(set(entry['answer_wrong'] + data['answer_wrong']))
                found = True
                break
        
        if not found:
            database.append(data)
    
    # Write the updated data back to the database file
    with open(filename, 'w') as file:
        json.dump(database, file, indent=4)

def pull_from_database(filename, data_name):
    """
    Pulls data from the database by name.
    """
    data_name = clean_text(data_name)
    
    # Load existing data from the database file
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            database = json.load(file)
    else:
        return None

    # Search for the data with the given name
    for entry in database:
        if entry['name'] == data_name:
            return entry
    
    return None

def compare_elements(element1, element2):
    # Normalize and compare the string representations
    return clean_text(element1) == clean_text(element2)

def set_answer_solved_by_index(datalist, target_index, val : bool):
    for item in datalist:
        if item['index'] == target_index:
            item['solved'] = val
            item['answer_right'] = item['answer']

def get_data_by_index(datalist, target_index):
    for item in datalist:
        if item['index'] == target_index:
            return item
    return None

while True:
    chrome_options = Options() # You can disable/enable option below if you like to
    chrome_options.add_argument("--headless")  # Disable driver window (also prints a lot of warnings in console)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")   # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-infobars")  # Disable infobars

    print('Cycle started:', end=' ')
    print(datetime.now().strftime('%H:%M:%S'))
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(login_url)

        # Find the username and password fields and log in
        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Wait for the login to complete and the main page to load
        wait = WebDriverWait(driver, 5)

        print('\nStarting test id:'+target_url[-2:])
        # Navigate to the target page
        driver.get(target_url)
        wait.until(EC.url_to_be(target_url))

        # Locate the button within the form
        form = driver.find_element(By.TAG_NAME, 'form')
        if not form:
            print('Form was not found.')
            exit() 

        form_button = form.find_element(By.TAG_NAME, "button")
        if not form_button:
            print('Start test button not found')
            exit()

        isStarted = False
        if 'Продолжить последнюю попытку' in form_button.text:
            isStarted = True

        form_button.click()

        if not isStarted:
            time.sleep(3)

            if 'startattempt' in driver.current_url:
                form_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][name="submitbutton"]')
                if not form_button:
                    print('Second page tart test button not found')
                    exit()

                form_button.click()
            else:
                # Wait for dialogue element to appear
                dialogue_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'moodle-dialogue-base')))
                if not dialogue_element:
                    print('Element with class "moodle-dialogue-base" not found.')
                    exit()

                # Find the form within the dialogue element
                form = dialogue_element.find_element(By.TAG_NAME, 'form')
                if not form:
                    print('Form was not found.')
                    exit() 

                form_button = form.find_element(By.XPATH, "//input[@type='submit']")
                if not form_button:
                    print('Pop up start test button not found')
                    exit()

                form_button.click()

        current_data = []

        for page in range(0, pageCount):
            if 'https://phys-online.ru/mod/quiz/summary.php' in driver.current_url or 'https://phys-online.ru/mod/quiz/review.php' in driver.current_url:
                print('\nTest finished\n')
                break

            # Wait for the next page to load completely
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'que')))
            time.sleep(3)

            # Get the page source and parse it with BeautifulSoup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find all elements with class 'que'
            ques = soup.find_all(class_='que')
            que_count = 0
            for que in ques:
                que_count += 1
                qText = que.find(class_='qtext')
                if not qText:
                    print('\nQuestion not found.')
                    continue
                
                paragraph = qText.find('p')
                if not paragraph:
                    print('\nQuestion paragraph not found.')
                    continue
                
                print('\nTrying to find question in database')
                current_question = pull_from_database('data_'+target_url[-2:]+'.json', paragraph.get_text())
                current_answer = ''
                isAnswered = False
                if current_question and current_question['solved'] == True:
                    current_answer = current_question['answer_right']
                    #print(paragraph.get_text())
                    #print(current_answer)

                    answers = que.find(class_='answer')
                    if not answers:
                        print('None answer fields were found.')
                        continue

                    answer_children = list(answers.find_all('div', class_=["flex-fill", "ml-1"]))
                    answer_children = [child for child in answer_children if child.name is not None]

                    if not answer_children or len(answer_children) == 0:
                        print('Did not found any answer_children')
                        continue

                    for answer in answer_children:
                        if compare_elements(answer.text, current_answer):
                            current_answer = answer
                            isAnswered = True
                            print(que_count + page * 5, ': Answer found in database')
                            current_data.append({"name":paragraph.get_text(),"index": que_count + page * 5,"solved":True ,"answer": str(current_answer.text)})
                            break
                        
                    if not isAnswered:
                        for k in range(10000):
                            answer_index = random.randint(0, len(answer_children) - 1)
                            isAnswered = True
                            current_answer = answer_children[answer_index]
                            if clean_text(answer_children[answer_index].text) not in current_question['answer_wrong']:
                                break
                        print(que_count + page * 5, ': Answer was randomly generated')

                        current_data.append({"name":paragraph.get_text(),"index": que_count + page * 5,"solved":False ,"answer": str(answer_children[answer_index].text)})
                else:
                    answers = que.find(class_='answer')
                    if not answers:
                        print('None answer fields were found.')
                        continue

                    answer_children = list(answers.find_all('div', class_=["flex-fill", "ml-1"]))
                    answer_children = [child for child in answer_children if child.name is not None]

                    if not answer_children or len(answer_children) == 0:
                        print('Did not found any answer_children')
                        continue

                    if not current_question:
                        answer_index = random.randint(0, len(answer_children) - 1)
                        current_answer = answer_children[answer_index]
                        isAnswered = True
                    else:
                        for k in range(10000):
                            answer_index = random.randint(0, len(answer_children) - 1)
                            current_answer = answer_children[answer_index]
                            isAnswered = True
                            if clean_text(answer_children[answer_index].text) not in current_question['answer_wrong']:
                                break
                            #else:
                                #print(que_count + page * 5, ': Generated answer is found to be wrong.')
                    print(que_count + page * 5, ': Answer randomly generated')

                    current_data.append({"name":paragraph.get_text(),"index": que_count + page * 5,"solved":False ,"answer": str(answer_children[answer_index].text)})

                if isAnswered:
                    # Click the radio button within the current_answer
                    radio_button = current_answer.parent.parent.find('input', {'type': 'radio'})
                    if not radio_button:
                        print('Radio button for answer was not found.')
                        continue

                    radio_button_id = radio_button['id']
                    radio_button_element = driver.find_element(By.ID, radio_button_id)
                    radio_button_element.click()

            form = driver.find_element(By.TAG_NAME, 'form')
            button_next = form.find_element(By.CSS_SELECTOR, 'input[type="submit"][name="next"]')

            if not button_next:
                print('Next page button not found.')
                exit()

            button_next.click()

        if 'https://phys-online.ru/mod/quiz/review.php' not in driver.current_url:
            form = driver.find_element(By.CSS_SELECTOR, 'form[action="https://phys-online.ru/mod/quiz/processattempt.php"]')
            if not form:
                print('Form for test submition not found.')
                exit()

            button_submit = form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

            if not button_submit:
                print('Submit test button not found.')
                exit()

            button_submit.click()

            dialogue_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'moodle-dialogue-base')))
            if not dialogue_element:
                print('Element with moodle-dialogue-base not found.')
                exit()

            button_submit = dialogue_element.find_element(By.CSS_SELECTOR, 'input[type="button"][value="Отправить всё и завершить тест"]')
            if not button_submit:
                print("Pop up submit test button not found.")
                exit()

            button_submit.click()

        all_answers = driver.find_element(By.CLASS_NAME, ('allquestionsononepage'))
        answer_children = all_answers.find_elements(By.XPATH, '*')

        if not answer_children:
            print('answer_children for test not found.')
            exit()

        print('\nAnswers are correct: ', end='')
        ans_index = 0
        rightAnsCount = 0
        wrong_answers = '\nAnswers change Solved to False: '
        for answer in answer_children:
            ans_index += 1
            if 'correct' in answer.get_attribute('class').split():
                set_answer_solved_by_index(current_data, ans_index, True)
                print(ans_index, end=' ')
                rightAnsCount+=1
            if 'incorrect' in answer.get_attribute('class').split() and get_data_by_index(current_data, ans_index)['solved']:
                set_answer_solved_by_index(current_data, ans_index, False)
                wrong_answers += str(ans_index) + ' '

        print('Total right answers: ', rightAnsCount)

        if has_numbers(wrong_answers):
            print(wrong_answers)

        push_to_database('data_'+target_url[-2:]+'.json', convert_to_database_format(current_data))
        print('\nData saved to data_'+target_url[-2:]+'.json')
        print('Cycle ended. Aproximate time of the next cycle:', end=' ')

        current_time = datetime.now()
        new_time = current_time + timedelta(seconds=sleepTime)
        print(new_time.strftime('%H:%M:%S'))
        print('\n')
    finally:
        # Wait for next cycle
        driver.close()
        driver.quit()
        time.sleep(sleepTime)