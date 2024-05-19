from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import random
import time
import json
import re

# URL of the login page and the target page
login_url = 'https://phys-online.ru/login/index.php'
target_url = 'https://phys-online.ru/mod/quiz/view.php?id=56'

# Your login credentials
username = ''
password = ''

# Path to your WebDriver
driver_path = ''  # Update with the correct path

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

def push_to_database(filename: str, data: List[Dict[str, Any]]) -> None:
    try:
        with open(filename, 'r') as jsonfile:
            existing_data = json.load(jsonfile)
    except FileNotFoundError:
        existing_data = []

    for item in data:
        existing_item = next((x for x in existing_data if x['name'] == item['name']), None)
        
        if existing_item:
            existing_wrong = existing_item.get('answer_wrong', [])
            if isinstance(existing_wrong, int):
                existing_wrong = [existing_wrong]
            unique_wrong_values = [wrong for wrong in item['answer_wrong'] if wrong not in existing_wrong]
            existing_wrong.extend(unique_wrong_values)
            existing_item['answer_wrong'] = existing_wrong
            existing_item['solved'] = item['solved']
            existing_item['answer_right'] = item['answer_right']
        else:
            existing_data.append(item)

    with open(filename, 'w') as jsonfile:
        json.dump(existing_data, jsonfile, indent=4)

def normalize_string(s: str) -> str:
    return ' '.join(s.split())

def pull_from_database(filename: str, item_name: str) -> Optional[Dict[str, Any]]:
    try:
        with open(filename, 'r') as jsonfile:
            existing_data = json.load(jsonfile)
    except FileNotFoundError:
        print("Database file not found.")
        return None

    normalized_item_name = normalize_string(item_name)
    return next((item for item in existing_data if normalize_string(item['name']) == normalized_item_name), None)

def normalize_element(element):
    # Convert element to string and remove extra whitespace and newlines
    html_str = str(element)
    # Remove leading/trailing whitespace and newlines
    html_str = html_str.strip()
    # Replace multiple spaces with a single space
    html_str = re.sub(r'\s+', ' ', html_str)
    return html_str

def compare_elements(element1, element2):
    # Normalize and compare the string representations
    return normalize_element(element1) == normalize_element(element2)

def set_answer_solved_by_index(data, target_index):
    for item in data:
        if item['index'] == target_index:
            item['solved'] = True
            item['answer_right'] = item['answer']

while True:
    # Start a Selenium WebDriver session
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

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
        if form_button.text == 'Продолжить последнюю попытку':
            isStarted = True

        form_button.click()

        if not isStarted:
            time.sleep(3)

            
            if 'startattempt' in driver.current_url:
                form_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][class="btn-primary"]')
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

        for page in range(0, 3):
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
                    print('Question not found.')
                    continue
                
                paragraph = qText.find('p')
                if not paragraph:
                    print('Question paragraph not found.')
                    continue
                
                print('\nTrying to pull question from database')
                current_question = pull_from_database('data_'+target_url[-2:]+'.json', paragraph.get_text())
                current_answer = ''
                isAnswered = False
                if current_question and current_question['solved'] == True:
                    current_answer = current_question['answer_right']

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
                        if compare_elements(answer, current_answer):
                            isAnswered = True
                            print('Answer found in database')
                            break
                        
                    if not isAnswered:
                        for k in range(10000):
                            answer_index = random.randint(0, len(answer_children) - 1)
                            isAnswered = True
                            if answer_children[answer_index] not in current_question['answer_wrong']:
                                current_answer = answer_children[answer_index]
                                break
                        print('Answer randomly generated')

                        current_data.append({"name":paragraph.get_text(),"index": que_count + page * 5,"solved":False ,"answer": str(answer_children[answer_index])})
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

                    for k in range(10000):
                            answer_index = random.randint(0, len(answer_children) - 1)
                            current_answer = answer_children[answer_index]
                            isAnswered = True
                            if current_question and answer_children[answer_index] not in current_question['answer_wrong']:
                                break
                    print('Answer randomly generated')

                    current_data.append({"name":paragraph.get_text(),"index": que_count + page * 5,"solved":False ,"answer": str(answer_children[answer_index])})

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

        print('Answers are correct: ', end='')
        ans_index = 0
        for answer in answer_children:
            ans_index += 1
            if 'correct' in answer.get_attribute('class').split():
                set_answer_solved_by_index(current_data, ans_index)
                print(ans_index, end=' ')

        push_to_database('data_'+target_url[-2:]+'.json', convert_to_database_format(current_data))
        print('\n\nData saved to data_'+target_url[-2:]+'.json')
        print('Waiting for next cycle')

    finally:
        # Wait for next cycle
        driver.quit()
        time.sleep(300)