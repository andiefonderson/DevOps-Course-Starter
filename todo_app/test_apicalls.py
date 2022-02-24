import os
import pytest
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
    assert response.status_code == 200
    assert 'Test card' in response.data.decode()
    assert 'Test in progress' in response.data.decode()

def test_delete_task(monkeypatch, client):
    monkeypatch.setattr(requests, 'post', delete_task_stub)
    response = client.post('delete/123')

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

def get_lists_stub(url, params):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists/':
        fake_response_data = fake_response()
    return StubResponse(fake_response_data)
    
def delete_task_stub(url, card_id):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/cards/123/':
        fake_response_data = fake_delete_response()
    return StubResponse(fake_response_data)

def fake_response():
    return [
        {'id': '123abc',
        'name': 'Not Started',
        'cards': [{'id': '456', 'name': 'Test card', 'desc': 'Test card description', 'closed': False, 'due': None, 'dueComplete': False}]},
        {'id': '456def',
        'name': 'In Progress',
        'cards': [{'id': '098', 'name': 'Test in progress', 'desc': 'Still ongoing', 'closed': False, 'due': '2022-02-22T05:00:00.000Z', 'dueComplete': False}]},
        {'id': '789ghi',
        'name': 'Complete',
        'cards': [{'id': '639', 'name': 'Test done', 'desc': 'This has been finished.', 'closed': False, 'due': None, 'dueComplete': True}]}
        ]

def fake_delete_response():
    return { 'limits': {} }