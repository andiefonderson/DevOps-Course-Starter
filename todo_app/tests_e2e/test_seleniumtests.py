from optparse import Option
import os, pytest, requests
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from threading import Thread
from todo_app import app

def create_board(board_name):
    url = 'https://api.trello.com/1/boards/'
    id_organisation = os.getenv('TRELLO_IDORGANISATION')
    api_params = params({ 'idOrganization': id_organisation, 'name': board_name })
    print(api_params)
    response = requests.post(url, api_params).json()
    board_id = response['id']
    rename_lists(board_id)
    return board_id

def delete_board(board_id):
    api_key = os.getenv('TRELLO_KEY')
    api_token = os.getenv('TRELLO_TOKEN')
    url = f'https://api.trello.com/1/boards/{board_id}?key={api_key}&token={api_token}'
    response = requests.delete(url)
    if response.status_code == 200:
        print('Board successfully deleted')
    elif response.status_code == 400:
        print('Invalid board ID - please try again')
    else: 
        print(response.status_code)

def rename_lists(board_id):
    url = f'https://api.trello.com/1/boards/{board_id}/lists/'
    response = requests.get(url,params({ 'fields': 'name'})).json()
    for list in response:
        change_list_name(list['id'], list['name'])

def change_list_name(list_id, list_name):
    url = f'https://api.trello.com/1/lists/{list_id}'
    match list_name:
        case 'To Do':
            new_list_name = 'Not Started'
            os.environ['NOT_STARTED_LIST_ID'] = list_id
        case 'Doing':
            new_list_name = 'In Progress'
            os.environ['IN_PROGRESS_LIST_ID'] = list_id
        case 'Done':
            new_list_name = 'Complete'
            os.environ['COMPLETE_LIST_ID'] = list_id
    response = requests.put(url, params({ 'name': new_list_name})).json()
    print(f'List \'{list_name}\' renamed to \'{new_list_name}\'')

def params(add_params):
    api_key = os.getenv('TRELLO_KEY')
    api_token = os.getenv('TRELLO_TOKEN')    
    api_params = { 'key': api_key, 'token': api_token }
    params = api_params.copy()
    params.update(add_params)
    if add_params == '':
        return api_params
    else:
        return params

@pytest.fixture(scope='module')
def app_with_test_board():
    file_path = find_dotenv('.env')
    os.environ['FLASK_ENV'] = "testing"
    load_dotenv(file_path, override=True)
    new_board_id = create_board('Selenium Test Board')
    os.environ['TRELLO_BOARD_ID'] = new_board_id

    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear Down
    thread.join(1)
    delete_board(new_board_id)

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("-headless")
    with webdriver.Firefox(options=options) as driver:
        yield driver

def test_task_journey(driver, app_with_test_board):    
    # Checks that the app can start up properly after creating a board
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    # Checks that a task can be added
    test_task_title = 'This is a test task'
    add_test_task(driver, test_task_title)
    task = driver.find_element(By.CLASS_NAME, 'task-title')
    assert task.text == test_task_title

    # Checks that a task can be edited and that its changes persists on the index page
    task.click()
    edited_task_title = 'This is an edited test task'
    edit_due_date = '22/02/2022'
    edit_task(driver, edited_task_title, 'Complete', edit_due_date)
    refreshed_task = driver.find_element(By.CLASS_NAME, 'task-title')
    assert refreshed_task.text == edited_task_title
    assert driver.find_element(By.CLASS_NAME, 'task-status').text == 'Complete'
    assert driver.find_element(By.CLASS_NAME, 'task-due-text').text == 'Completed today'

    # Checks that a task can be deleted and that the right task is being deleted
    refreshed_task.click()
    click_button(driver, 'delete-button')
    assert driver.find_element(By.CLASS_NAME, 'card-title').text == edited_task_title
    click_button(driver, 'delete-task-button')
    assert not driver.find_elements (By.CLASS_NAME, 'task-title') == None 

def add_test_task(driver, task_text):
    to_do_button = driver.find_element(By.NAME, 'add-to-do-task-button')
    new_task_title_textbox = driver.find_element(By.NAME, 'to-do-title')
    new_task_notes_textbox = driver.find_element(By.NAME, 'to-do-notes')
    submit_button = driver.find_element(By.NAME, 'submit-task')

    to_do_button.click()
    new_task_title_textbox.send_keys(task_text)
    new_task_notes_textbox.send_keys('These are the notes for the test task.')
    submit_button.click()

def edit_task(driver, edited_title, status, due_date):
    click_button(driver, 'edit-button')
    task_title_textbox = driver.find_element(By.NAME, 'task-title')
    task_title_textbox.clear()
    task_title_textbox.send_keys(edited_title)
    select = Select(driver.find_element(By.NAME, 'task-status'))
    select.select_by_value(status)
    driver.find_element(By.NAME, 'task-due-date').send_keys(due_date)
    click_button(driver, 'submit-amend-task')
    click_button(driver, 'back-button')

def delete_task(driver):
    click_button(driver, 'delete-button')


def click_button(driver, button_name):
    return driver.find_element(By.NAME, button_name).click()