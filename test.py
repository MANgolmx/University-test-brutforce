'''import requests
from bs4 import BeautifulSoup

# URL of the login page
login_url = 'https://phys-online.ru/login/index.php'

# URL of the page you want to scrape after logging in
target_url = 'https://phys-online.ru/mod/quiz/attempt.php?attempt=590656&cmid=56'

# Your login credentials
username = 'misammmmm@inbox.ru'
password = '#89OO3657228Mm'

# Start a session
session = requests.Session()

# Retrieve the login page
login_page = session.get(login_url)
login_soup = BeautifulSoup(login_page.content, 'html.parser')

# Find the login form and extract form data
login_form = login_soup.find('form')
login_action = login_form['action']  # The action URL for the form submission
login_method = login_form['method']  # The method for the form submission, typically 'POST'

# Prepare the payload with form data
payload = {}
for input_tag in login_form.find_all('input'):
    input_name = input_tag.get('name')
    input_value = input_tag.get('value', '')
    if input_name == 'username':
        input_value = username
    elif input_name == 'password':
        input_value = password
    payload[input_name] = input_value

# Perform the login
login_response = session.post(login_action, data=payload)

# Check if login was successful by verifying the response
if login_response.url == login_url or 'login' in login_response.url:
    print('Login failed. Please check your credentials and try again.')
else:
    print('Login successful.')

    # Now access the target page
    target_response = session.get(target_url)
    target_soup = BeautifulSoup(target_response.content, 'html.parser')

    # Function to find elements with specific text
    def find_elements_with_text(parent, text):
        matching_elements = []
        for child in parent.find_all(string=True):
            if text in child:
                matching_elements.append(child.parent)
        return matching_elements

    # Specify the class of the parent element
    parent_class = 'info'

    # Find the parent element with the specified class
    parent_element = target_soup.find(class_=parent_class)

    # Check if the parent element is found
    if parent_element:
        # Specify the text you are searching for
        search_text = 'Вопрос '

        # Find all elements with the specific text within the parent element's children
        elements_with_text = find_elements_with_text(parent_element, search_text)

        # Print the found elements
        for element in elements_with_text:
            print(element)
    else:
        print(f'Element with class "{parent_class}" not found.')

    print(target_soup)


import requests
from bs4 import BeautifulSoup

# URL of the login page and the target page
login_url = 'https://phys-online.ru/login/index.php'
target_url = 'https://phys-online.ru/mod/quiz/view.php?id=56'

# Your login credentials
username = 'misammmmm@inbox.ru'
password = '#89OO3657228Mm'

# Start a session
session = requests.Session()

# Retrieve the login page
login_page = session.get(login_url)
login_soup = BeautifulSoup(login_page.content, 'html.parser')

# Find the login form and extract form data
login_form = login_soup.find('form')
if not login_form:
    print('Login form not found on the login page.')
    exit()

login_action = login_form['action']  # The action URL for the form submission
login_method = login_form['method']  # The method for the form submission, typically 'POST'

# Prepare the payload with form data
payload = {}
for input_tag in login_form.find_all('input'):
    input_name = input_tag.get('name')
    input_value = input_tag.get('value', '')
    if input_name == 'username':
        input_value = username
    elif input_name == 'password':
        input_value = password
    payload[input_name] = input_value

# Perform the login
login_action_url = login_action if login_action.startswith('http') else f'https://phys-online.ru{login_action}'
login_response = session.post(login_action_url, data=payload)

# Check if login was successful by verifying the response
if login_response.url == login_url or 'login' in login_response.url:
    print('Login failed. Please check your credentials and try again.')
    exit()
else:
    print('Login successful.')

# Now access the target page
target_response = session.get(target_url)
target_soup = BeautifulSoup(target_response.content, 'html.parser')

# Find the element with class 'moodle-dialogue-base' and attribute 'aria-hidden=true'
dialogue_element = target_soup.find(class_='moodle-dialogue-base', attrs={'aria-hidden': 'true'})
if not dialogue_element:
    print('Element with class "moodle-dialogue-base" not found on the target page.')
    print(target_soup)
    exit()

# Find the form within the dialogue element
form = dialogue_element.find('form')
if not form:
    print('Form within the dialogue element not found.')
    exit()

form_action = form['action']  # The action URL for the form submission
form_method = form['method']  # The method for the form submission, typically 'POST'

# Prepare the payload with form data
form_payload = {}
for input_tag in form.find_all('input'):
    input_name = input_tag.get('name')
    input_value = input_tag.get('value', '')
    form_payload[input_name] = input_value

# Perform the form submission
form_action_url = form_action if form_action.startswith('http') else f'https://phys-online.ru{form_action}'
if form_method.lower() == 'post':
    form_response = session.post(form_action_url, data=form_payload)
else:
    form_response = session.get(form_action_url, params=form_payload)

# Check if form submission was successful
if form_response.status_code == 200:
    print('Form submitted successfully.')

    # Parse the redirected page
    redirected_soup = BeautifulSoup(form_response.content, 'html.parser')

    # Function to find elements with specific text
    def find_elements_with_text(parent, text):
        matching_elements = []
        for child in parent.find_all(string=True):
            if text in child:
                matching_elements.append(child.parent)
        return matching_elements

    # Specify the class of the parent element
    parent_class = 'specific-class'

    # Find the parent element with the specified class
    parent_element = redirected_soup.find(class_=parent_class)

    # Check if the parent element is found
    if parent_element:
        # Specify the text you are searching for
        search_text = 'specific text'

        # Find all elements with the specific text within the parent element's children
        elements_with_text = find_elements_with_text(parent_element, search_text)

        # Print the found elements
        for element in elements_with_text:
            print(element)
    else:
        print(f'Element with class "{parent_class}" not found on the redirected page.')
else:
    print('Form submission failed.')


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# Sample HTML content
html_content = """
<div class="parent">
    <div class="chjj">
        <div class ="child">Hello</div>
    </div>
    <div class="child">Child 2</div>
    <div class="child">Child 3</div>
</div>
"""

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the parent element containing all answers
all_answers = soup.find_element(By.CLASS_NAME, 'parent')

# Find all direct children of the parent element
answer_children = all_answers.find_elements(By.XPATH, './*')  # Select all direct children elements

# Loop through each direct child
for answer in answer_children:
    # Check if the answer contains the class 'correct'
    if 'correct' in answer.get_attribute('class'):
        print("This answer is correct.")
    else:
        print("This answer is not correct.")

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

str = """
 Какая из предложенных формул является уравнением состояния идеального газа (уравнение Менделеева-Клапейрона)?
"""

str1 ="""
<p> По какой из перечисленных формул можно рассчитать среднюю энергию теплового движения молекулы произвольного газа? (здесь <span class="MathJax_Preview" style="display: none;"></span><span class="MathJax" id="MathJax-Element-37-Frame" tabindex="0" style=""><nobr><span class="math" id="MathJax-Span-550" style="width: 0.405em; display: inline-block;"><span style="display: inline-block; position: relative; width: 0.348em; height: 0px; font-size: 116%;"><span style="position: absolute; clip: rect(1.44em, 1000.29em, 2.474em, -999.997em); top: -2.296em; left: 0em;"><span class="mrow" id="MathJax-Span-551"><span class="mi" id="MathJax-Span-552" style="font-family: MathJax_Math-italic;">i</span></span><span style="display: inline-block; width: 0px; height: 2.302em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.063em; border-left: 0px solid; width: 0px; height: 0.937em;"></span></span></nobr></span><script type="math/tex" id="MathJax-Element-37">i</script> - число степеней свободы молекул газа,  <span class="MathJax_Preview" style="display: none;"></span><span class="MathJax" id="MathJax-Element-38-Frame" tabindex="0" style=""><nobr><span class="math" id="MathJax-Span-553" style="width: 0.865em; display: inline-block;"><span style="display: inline-block; position: relative; width: 0.75em; height: 0px; font-size: 116%;"><span style="position: absolute; clip: rect(1.44em, 1000.75em, 2.474em, -999.997em); top: -2.296em; left: 0em;"><span class="mrow" id="MathJax-Span-554"><span class="mi" id="MathJax-Span-555" style="font-family: MathJax_Math-italic;">R</span></span><span style="display: inline-block; width: 0px; height: 2.302em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.063em; border-left: 0px solid; width: 0px; height: 0.937em;"></span></span></nobr></span><script type="math/tex" id="MathJax-Element-38">R</script>-универсальная газовая постоянная, <span class="MathJax_Preview" style="display: none;"></span><span class="MathJax" id="MathJax-Element-39-Frame" tabindex="0" style=""><nobr><span class="math" id="MathJax-Span-556" style="width: 0.635em; display: inline-block;"><span style="display: inline-block; position: relative; width: 0.52em; height: 0px; font-size: 116%;"><span style="position: absolute; clip: rect(1.44em, 1000.52em, 2.474em, -999.997em); top: -2.296em; left: 0em;"><span class="mrow" id="MathJax-Span-557"><span class="mi" id="MathJax-Span-558" style="font-family: MathJax_Math-italic;">k</span></span><span style="display: inline-block; width: 0px; height: 2.302em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.063em; border-left: 0px solid; width: 0px; height: 0.937em;"></span></span></nobr></span><script type="math/tex" id="MathJax-Element-39">k</script> - постоянная Больцмана,  <span class="MathJax_Preview" style="display: none;"></span><span class="MathJax" id="MathJax-Element-40-Frame" tabindex="0" style=""><nobr><span class="math" id="MathJax-Span-559" style="width: 0.693em; display: inline-block;"><span style="display: inline-block; position: relative; width: 0.578em; height: 0px; font-size: 116%;"><span style="position: absolute; clip: rect(1.67em, 1000.58em, 2.474em, -999.997em); top: -2.296em; left: 0em;"><span class="mrow" id="MathJax-Span-560"><span class="mi" id="MathJax-Span-561" style="font-family: MathJax_Math-italic;">ν<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.06em;"></span></span></span><span style="display: inline-block; width: 0px; height: 2.302em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.063em; border-left: 0px solid; width: 0px; height: 0.67em;"></span></span></nobr></span><script type="math/tex" id="MathJax-Element-40">\nu</script> - количество вещества, <span class="MathJax_Preview" style="display: none;"></span><span class="MathJax" id="MathJax-Element-41-Frame" tabindex="0" style=""><nobr><span class="math" id="MathJax-Span-562" style="width: 0.807em; display: inline-block;"><span style="display: inline-block; position: relative; width: 0.693em; height: 0px; font-size: 116%;"><span style="position: absolute; clip: rect(1.44em, 1000.69em, 2.474em, -999.997em); top: -2.296em; left: 0em;"><span class="mrow" id="MathJax-Span-563"><span class="mi" id="MathJax-Span-564" style="font-family: MathJax_Math-italic;">T<span style="display: inline-block; overflow: hidden; height: 1px; width: 0.118em;"></span></span></span><span style="display: inline-block; width: 0px; height: 2.302em;"></span></span></span><span style="display: inline-block; overflow: hidden; vertical-align: -0.063em; border-left: 0px solid; width: 0px; height: 0.937em;"></span></span></nobr></span><script type="math/tex" id="MathJax-Element-41">T</script> - абсолютная температура газа)</p>
"""

element = pull_from_database("data_56.json", str)

if not element:
    print('Not found')

if element['solved'] == True:
    print('True')
else:
    print('False')
    '''

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

def normalize_string(s: str) -> str:
    return ' '.join(s.split())

def clean_text(text: str) -> str:
        if text is None:
            return ""
        text_copy = text
        return text_copy.replace(' ', '').replace('\n', '')

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

def pull_from_database(filename: str, item_name: str) -> Optional[Dict[str, Any]]:
    try:
        with open(filename, 'r') as jsonfile:
            existing_data = json.load(jsonfile)
    except FileNotFoundError:
        print("Database file not found.")
        return None

    normalized_item_name = clean_text(normalize_string(item_name))
    return next((item for item in existing_data if clean_text(normalize_string(item['name'])) == normalized_item_name), None)

# Test data
data = [
    {
        "name": "Test Item 1",
        "answer_wrong": ["wrong1", "wrong2"],
        "answer_right": "correct1",
        "solved": True
    },
    {
        "name": "Test Item 2",
        "answer_wrong": ["wrong3"],
        "answer_right": "Corrrwec   gasdgsg   nn\\n\\n\\n\n\n\n\n      h",
        "solved": False
    },
    {
        "name": "Test Item 10",
        "answer_wrong": [],
        "answer_right": None,
        "solved": False
    }
]

# Push to database
push_to_database('database.json', data)

element = "String with spaces"
print(clean_text(element))
print(element)
