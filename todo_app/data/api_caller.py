from flask import json
import os
import requests

api_key = os.getenv('TRELLO_KEY')
api_token = os.getenv('TRELLO_TOKEN')
board_id = os.getenv('TRELLO_BOARD_ID')

def get_tasks():
    api_url = 'https://api.trello.com/1/boards/' + board_id + '/lists/'
    auth_string = {"key":api_key, 
        "token":api_token, 
        "fields":"name", 
        "cards":"all", 
        "card_fields":"name,desc"}
    response = requests.get(api_url, params=auth_string)
    list_cards = json.loads(response.text)
    
    todo_tasks = []

    for list in list_cards:
        for card in list['cards']:
            task = { 'id': card['id'], 'title': card['name'], 'status': list['name'], 'notes': card['desc']}
            todo_tasks.append(task)
    
    return todo_tasks

def get_task(id):
    tasks = get_tasks()
    for task in tasks:
        if id == task['id']:
            return task
