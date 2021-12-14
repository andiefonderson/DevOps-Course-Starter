from flask import json
import os
import requests

from todo_app.data.Item import Item

api_key = os.getenv('TRELLO_KEY')
api_token = os.getenv('TRELLO_TOKEN')
board_id = os.getenv('TRELLO_BOARD_ID')
not_started_listid = os.getenv('NOT_STARTED_LIST_ID')
in_progress_listid = os.getenv('IN_PROGRESS_LIST_ID')
complete_listid = os.getenv('COMPLETE_LIST_ID')

def get_tasks():
    api_params = {"key":api_key, 
        "token":api_token, 
        "fields":"name", 
        "cards":"all", 
        "card_fields":"name,desc,closed,due,dueComplete"}
    list_cards = requests.get(api_url('list'), params=api_params).json()
    
    todo_tasks = []

    for list in list_cards:
        for card in list['cards']:
            if card['closed']:
                continue
            else:
                task = Item.from_trello_card(card, list)
                todo_tasks.append(task)
    
    return todo_tasks

def get_task(id):
    tasks = get_tasks()
    for task in tasks:
        if id == task.id:
            return task

def create_task(task_name, task_notes=""):
    api_params = { 'key':api_key,
        'token':api_token,
        'idList': not_started_listid,
        'name': task_name,
        'desc': task_notes }
    task = requests.post(api_url('card'), data=api_params).json()
    return get_tasks()

def edit_task(task):
    url_call = api_url('cardID', task.id)      
    api_params= { 'key':api_key,
        'token':api_token,
        'name':task.name,
        'desc':task.notes,
        'idList':list_id(task.status)}
    response = requests.put(url_call, data=api_params)
    return task

def delete_from_tasklist(id):
    url_call = api_url('cardID', id)
    api_params = { 'key':api_key, 'token':api_token }
    response = requests.delete(url_call, params=api_params)
    return response


def api_url(board_list_or_card, card_ID=""):
    match board_list_or_card:
        case 'board':
            return 'https://api.trello.com/1/boards/'
        case 'list':
            return 'https://api.trello.com/1/boards/' + board_id + '/lists/'
        case 'card':
            return 'https://api.trello.com/1/cards/'
        case 'cardID':
            return 'https://api.trello.com/1/cards/' + card_ID + '/'

def list_id(status):
    match status:
        case 'Not Started':
            return not_started_listid
        case 'In Progress':
            return in_progress_listid
        case 'Complete':
            return complete_listid