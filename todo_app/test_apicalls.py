import os, pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from todo_app.data.trello_items import *

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_lists_stub)
    response = client.get('/')
    page_data = response.data.decode()
    assert response.status_code == 200
    assert 'Test card' in page_data
    assert 'Test in progress' in page_data

def test_return_task(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_lists_stub)
    response = client.get('/task/639')
    page_data = response.data.decode()
    assert 'Test done' in page_data
    assert not 'Test in progress' in page_data

def test_add_task(monkeypatch, client):
    monkeypatch.setattr(requests, 'post', add_task_stub)
    monkeypatch.setattr(requests, 'get', get_amended_lists_stub)
    page_data = { 'to-do-title': 'New task name', 'task-due-date': '', 'to-do-notes': 'Random notes' }
    response = client.post('/', data=page_data, follow_redirects = True)

    page_data = response.data.decode()
    assert 'New task name' in page_data

def test_delete_task(monkeypatch, client):
    monkeypatch.setattr(requests, 'post', delete_task_stub)
    data = { 'delete-task-button': True }
    monkeypatch.setattr(requests, 'get', post_delete_tasklist_stub)
    response = client.post(f'/delete/098', data=data, follow_redirects = True)
    reply = client.post(f'/delete/wow', data=data)
    assert not 'Test in progress' in response.data.decode()
    assert not reply.status_code == 200

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

def get_lists_stub(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    target_url = f'https://api.trello.com/1/boards/{test_board_id}/lists/'
    return retrieve_stub_response(url, target_url, fake_response())

def get_amended_lists_stub(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    target_url = f'https://api.trello.com/1/boards/{test_board_id}/lists/'
    return retrieve_stub_response(url, target_url, amended_fake_response())

def add_task_stub(url, data):
    return retrieve_stub_response(url, 'https://api.trello.com/1/cards/', add_to_tasks_fake_response(data))

def delete_task_stub(url, data):
    return retrieve_stub_response(url, 'https://api.trello.com/1/cards/098/', delete_task_fake_response())

def post_delete_tasklist_stub(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    target_url = f'https://api.trello.com/1/boards/{test_board_id}/lists/'
    return retrieve_stub_response(url, target_url, post_delete_fake_response())

def retrieve_stub_response(url, target_url, list):
    fake_response_data = None
    if url == target_url:
        fake_response_data = list
    return StubResponse(fake_response_data)

def fake_response():
    return [
        {'id': '123abc',
        'name': 'Not Started',
        'cards': [{'id': '456', 'name': 'Test card', 'desc': 'Test card description', 'closed': False, 'due': None, 'dueComplete': False, 'dateLastActivity': None }]},
        {'id': '456def',
        'name': 'In Progress',
        'cards': [{'id': '098', 'name': 'Test in progress', 'desc': 'Still ongoing', 'closed': False, 'due': '2022-02-22T05:00:00.000Z', 'dueComplete': False, 'dateLastActivity': None }]},
        {'id': '789ghi',
        'name': 'Complete',
        'cards': [{'id': '639', 'name': 'Test done', 'desc': 'This has been finished.', 'closed': False, 'due': None, 'dueComplete': True, 'dateLastActivity': None }]}
        ]

def response_contains_item(item_id, list):
    contains_item = False
    for status in list:
        for item in status:
            if item['id'] == item_id:
                contains_item = True
                break
    return contains_item

def add_to_tasks_fake_response(data):
    old_response = fake_response()
    new_item = { 'id': 827, 'name': data['name'], 'desc': data['desc'], 'closed': False, 'due': None, 'dueComplete': False, 'dateLastActivity': None }
    old_response[0]['cards'].append(new_item)
    return old_response

def amended_fake_response():
    old_response = fake_response()
    new_item = { 'id': 827, 'name': 'New task name', 'desc': 'Random notes', 'closed': False, 'due': None, 'dueComplete': False, 'dateLastActivity': None }
    old_response[0]['cards'].append(new_item)
    return old_response

def post_delete_fake_response():
    return [
        {'id': '123abc',
        'name': 'Not Started',
        'cards': [{'id': '456', 'name': 'Test card', 'desc': 'Test card description', 'closed': False, 'due': None, 'dueComplete': False, 'dateLastActivity': None }]},
        {'id': '456def',
        'name': 'In Progress',
        'cards': []},
        {'id': '789ghi',
        'name': 'Complete',
        'cards': [{'id': '639', 'name': 'Test done', 'desc': 'This has been finished.', 'closed': False, 'due': None, 'dueComplete': True, 'dateLastActivity': None }]}
        ]

def delete_task_fake_response():
    return { 'limits': {} }