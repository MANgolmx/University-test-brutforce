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
'''

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
