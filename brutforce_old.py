import pyautogui
from PIL import Image
import pytesseract
import time
import json
import random
from typing import List, Dict, Any, Optional

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

answers_pos = []
answers_text = []

#Taskbar is on the top
offset = 0

#Taskbar is on the bottom
#offset = -48

def take_screenshot_and_read_text(reg):
    # Take a screenshot of the specified region
    screenshot = pyautogui.screenshot(region=reg)

    screenshot_file = "screenshot.png"
    screenshot.save(screenshot_file)

    # Use pytesseract to read text from the screenshot
    extracted_text = pytesseract.image_to_string(screenshot, lang='rus')

    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)

    # Optionally, you can return the extracted text
    return extracted_text

def scroll_and_check_color(target_x, target_y, target_color):
    # Initial scroll position
    scroll_position = 0

    while True:
        # Scroll down 5 pixels
        pyautogui.scroll(-5)
        scroll_position += 5
        time.sleep(0.01)  # Adjust sleep time if needed

        # Get the color of the target point
        color = pyautogui.pixel(target_x, target_y)

        # Check if the color matches the target color
        if color == target_color:
            break

def count_answers(target_x, target_y):
    count = 0

    lastCount = False
    lastLastCount = False

    while target_y < 1080:
        color = pyautogui.pixel(target_x, target_y)
        
        if color == (255,255,255):
            if lastCount:
                if lastLastCount:
                    count -= 2
                    print("Answers counted:", count)
                    return count, target_y
                else:
                    count += 1
                    lastLastCount = True
            else:
                lastCount = True
                count+=1
        else:
            if lastLastCount:
                count -= 1
            lastCount = False
            lastLastCount = False

        if target_y > 1060  + offset:
            target_y -= 5
            pyautogui.scroll(-5)

        target_y += 5

def find_answers_pos_and_text(target_x, target_y):
    answers_pos.clear()
    answers_text.clear()
    lastCount = False
    lastLastCount = False

    while target_y < 1080:
        color = pyautogui.pixel(target_x, target_y)
        
        if color == (255,255,255):
            answers_pos.append(target_y)
            reg = (target_x + 10, target_y - 10, 1250, 25)
            answers_text.append(take_screenshot_and_read_text(reg))
            if lastCount:
                if lastLastCount:
                    answers_pos.pop()
                    answers_text.pop()
                    return
                else:
                    answers_pos.pop()
                    answers_text.pop()
                    lastLastCount = True
            else:
                lastCount = True
        else:
            #if lastLastCount:
            #    answers_pos.pop()
            lastCount = False
            lastLastCount = False

        if target_y < 5:
            return

        target_y -= 5

def push_to_database(filename: str, data: List[Dict[str, Any]]) -> None:
    try:
        with open(filename, 'r') as jsonfile:
            existing_data = json.load(jsonfile)
    except FileNotFoundError:
        existing_data = []

    for item in data:
        existing_item = next((x for x in existing_data if x['name'] == item['name'] and x['count'] == item['count']), None)
        
        if existing_item:
            existing_wrong = existing_item.get('wrong', [])
            if isinstance(existing_wrong, int):
                existing_wrong = [existing_wrong]
            unique_wrong_values = [wrong for wrong in item['wrong'] if wrong not in existing_wrong]
            existing_wrong.extend(unique_wrong_values)
            existing_item['wrong'] = existing_wrong
            existing_item['answer'] = item['answer']
            existing_item['right'] = item['right']
        else:
            existing_data.append(item)

    with open(filename, 'w') as jsonfile:
        json.dump(existing_data, jsonfile, indent=4)

def pull_from_database(filename: str, item_name: str) -> Optional[Dict[str, Any]]:
    try:
        with open(filename, 'r') as jsonfile:
            existing_data = json.load(jsonfile)
    except FileNotFoundError:
        print("Database file not found.")
        return None

    return next((item for item in existing_data if item['name'] == item_name), None)

data = []
indexes = []

target_x = 535
target_y = 640 + offset
target_color = (222, 226, 230)  # Grey color

time.sleep(3)

while True:

    #Loop for each test page
    for i in range(3):
        # Define the region of the screen to capture
        region = (575, 420 + offset, 1285, 55)

        extracted_text = take_screenshot_and_read_text(region)
        answers, finish_y = count_answers(596, 450  + offset)

        if answers > 0:
            find_answers_pos_and_text(596, finish_y - 15  + offset)

            item = pull_from_database("data.json", extracted_text)
            ans = ''
            ans_ind = 0

            if item:
                if item.get('answer') == True:
                   ans = item.get('right')
                   print('Found right answer in database:', ans)
                   if ans not in answers_text:
                       for k in range(10000):
                        ans_ind = random.randint(1, answers)
                        ans = answers_text[ans_ind]
                        if ans not in item.get('wrong'):
                            break
                else:
                    for k in range(10000):
                        ans_ind = random.randint(1, answers)
                        ans = answers_text[ans_ind]
                        if ans not in item.get('wrong'):
                            break
                    data.append({'name':extracted_text, 'count':answers, 'answer': False, 'right': 0, 'wrong':[0, ans]})
                    indexes.append({'name' : extracted_text, 'answer' : ans, 'index' : 5 * i})
                    print('Answer generated:', ans)
            else:
                ans_ind = random.randint(1, answers)
                ans = answers_text[ans_ind]
                data.append({'name':extracted_text, 'count':answers, 'answer': False, 'right': 0, 'wrong':[0, ans]})
                indexes.append({'name' : extracted_text, 'answer' : ans, 'index' : 5 * i})
                print('Answer generated:', ans)

            
            #print(answers_pos)

            pyautogui.moveTo(596, answers_pos[ans_ind - 1])
            pyautogui.click()
            pyautogui.moveTo(200, 200  + offset)

        #Loop for each question on the page
        for j in range(4):
            scroll_and_check_color(target_x, target_y, target_color)

            region = (575, target_y  + offset, 1285, 58)
            extracted_text = take_screenshot_and_read_text(region)

            answers, finish_y = count_answers(596, 680  + offset)

            if answers > 0:
                find_answers_pos_and_text(596, finish_y - 15  + offset)

                item = pull_from_database("data.json", extracted_text)
                ans = ''
                ans_ind = 0

                if item:
                    if item.get('answer') == True:
                        ans = item.get('right')
                        print('Found right answer in database:', ans)
                        if ans not in answers_text:
                            for k in range(10000):
                                ans_ind = random.randint(1, answers)
                                ans = answers_text[ans_ind]
                                if ans not in item.get('wrong'):
                                    break
                    else:
                        for k in range(10000):
                            ans_ind = random.randint(1, answers)
                            ans = answers_text[ans_ind]
                            if ans not in item.get('wrong'):
                                break
                        data.append({'name':extracted_text, 'count':answers, 'answer': False, 'right': 0, 'wrong':[0, ans]})
                        indexes.append({'name' : extracted_text, 'answer' : ans, 'index' : j + 1 + 5 * i})
                        print('Answer generated:', ans)
                else:
                    ans_ind = random.randint(1, answers)
                    ans = answers_text[ans_ind] 
                    data.append({'name':extracted_text, 'count':answers, 'answer': False, 'right': 0, 'wrong':[0, ans]})
                    indexes.append({'name' : extracted_text, 'answer' : ans, 'index' : j + 1 + 5 * i})
                    print('Answer generated:', ans)

                #print(answers_pos)

                pyautogui.moveTo(596, answers_pos[ans_ind - 1])
                pyautogui.click()
                pyautogui.moveTo(200, 200  + offset)

            pyautogui.scroll(-200)

        #Get to the end of the page
        pyautogui.scroll(-1000)

        if i == 0:
            x, y = 1780, 900  + offset
        else:
            x, y = 1780, 850  + offset

        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(5)


    pyautogui.scroll(-800)
    pyautogui.scroll(-800)
    pyautogui.moveTo(1150, 860  + offset)
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(1000, 710  + offset)
    pyautogui.click()
    time.sleep(5)

    #print(indexes)

    for i in range(8):
        color = pyautogui.pixel(95 + i * 35, 415  + offset)
        if color == (57, 132, 57):
            print("Right answer detected -", i + 1)

            for item_index in indexes:
                #print(item_index)
                if item_index['index'] == i:
                    #print('Found item_index: ', item_index['index'], item_index['name'])
                    # Find item in data with the same name
                    for item in data:
                        if item['name'] == item_index['name']:
                            item['answer'] = True
                            item['right'] = item_index['answer']
                            print('Changed data to True:', item_index['index'])
                    break

    for i in range(7):
        color = pyautogui.pixel(95 + i * 35, 462  + offset)
        if color == (57, 132, 57):
            print("Right answer detected -", i + 9)

            for item_index in indexes:
                #print(item_index)
                if item_index['index'] == i + 8:
                    #print('Found item_index: ', item_index['index'], item_index['name'])
                    # Find item in data with the same name
                    for item in data:
                        if item['name'] == item_index['name']:
                            item['answer'] = True
                            item['right'] = item_index['answer']
                            print('Changed data to True:', item_index['index'])
                    break

    push_to_database("data.json", data)

    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)
    pyautogui.scroll(-1000)

    pyautogui.moveTo(1800, 895  + offset)
    pyautogui.click()
    
    for i in range(5):
        pyautogui.scroll(-800)
        time.sleep(30)
        pyautogui.scroll(+800)
        time.sleep(30)

    color = pyautogui.pixel(1060, 285  + offset)
    if color == (14, 99, 174):
        pyautogui.moveTo(1060, 285  + offset)
        pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(1190, 285  + offset)
        pyautogui.click()
        time.sleep(5)
        pyautogui.moveTo(800, 530  + offset)
        pyautogui.click()
        time.sleep(5)

    pyautogui.moveTo(125, 100  + offset)
    pyautogui.click()
    time.sleep(5)

    pyautogui.moveTo(1150, 840  + offset)
    time.sleep(1)

    for i in range(50):
        pyautogui.scroll(-800)
    
    pyautogui.moveTo(1150, 840  + offset)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveTo(920, 725  + offset)
    pyautogui.click()
    time.sleep(5)