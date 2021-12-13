from flask import json
import os
import requests
from requests.api import get

api_key = os.getenv('TRELLO_KEY')
api_token = os.getenv('TRELLO_TOKEN')
board_id = os.getenv('TRELLO_BOARD_ID')
not_started_listid = os.getenv('NOT_STARTED_LIST_ID')
in_progress_listid = os.getenv('IN_PROGRESS_LIST_ID')
completed_listid = os.getenv('COMPLETED_LIST_ID')

def get_tasks():
    api_url = 'https://api.trello.com/1/boards/' + board_id + '/lists/'
    api_params = {"key":api_key, 
        "token":api_token, 
        "fields":"name", 
        "cards":"all", 
        "card_fields":"name,desc,closed"}
    response = requests.get(api_url, params=api_params)
    list_cards = json.loads(response.text)
    
    todo_tasks = []

    for list in list_cards:
        for card in list['cards']:
            if card['closed']:
                continue
            else:
                task = { 'id': card['id'], 'title': card['name'], 'status': list['name'], 'notes': card['desc']}
                todo_tasks.append(task)
    
    return todo_tasks

def get_task(id):
    tasks = get_tasks()
    for task in tasks:
        if id == task['id']:
            return task

def create_task(task_name, task_notes=""):
    api_url = 'https://api.trello.com/1/cards/'
    api_params = { 'key':api_key,
        'token':api_token,
        'idList': not_started_listid,
        'name': task_name,
        'desc': task_notes }
    task = requests.post(api_url, data=api_params)
    new_task = json.loads(task.text)
    return get_task(new_task['id'])