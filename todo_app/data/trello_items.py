from datetime import datetime
from flask import json
import os, requests
from requests import api

from todo_app.data.Item import Item

api_key = os.getenv('TRELLO_KEY')
api_token = os.getenv('TRELLO_TOKEN')
board_id = os.getenv('TRELLO_BOARD_ID')
not_started_listid = os.getenv('NOT_STARTED_LIST_ID')
in_progress_listid = os.getenv('IN_PROGRESS_LIST_ID')
complete_listid = os.getenv('COMPLETE_LIST_ID')

def get_tasks():
    api_params = {"fields":"name", 
        "cards":"all", 
        "card_fields":"name,desc,closed,due,dueComplete"}
    get_params = set_params(api_params)
    list_cards = requests.get(api_url('list'), params=get_params).json()
    
    todo_tasks = []

    for list in list_cards:
        for card in list['cards']:
            if card['closed']:
                continue
            else:
                task = Item.from_trello_card(card, list['name'])
                todo_tasks.append(task)
    
    return todo_tasks

def get_filtered_tasks(status):
    api_params = {"fields":"name,desc,closed,due,dueComplete"}
    get_params = set_params(api_params)
    card_list = requests.get(api_url('listID', list_id(status)), params=get_params).json()

    filtered_list = []

    for card in card_list:
        if card['closed']:
            continue
        else:
            task = Item.from_trello_card(card, status)
            filtered_list.append(task)

    return filtered_list



def get_task(id):
    tasks = get_tasks()
    for task in tasks:
        if id == task.id:
            return task

def create_task(task_name, task_due_date="", task_notes=""):
    api_params = { 'idList': not_started_listid,
        'name': task_name,
        'due': task_due_date,
        'desc': task_notes }
    create_params = set_params(api_params)
    response = requests.post(api_url('card'), data=create_params).json()
    return get_tasks()

def edit_task(task):
    url_call = api_url('cardID', task.id)   
    api_params= { 'name':task.name,
        'desc':task.notes,
        'idList':list_id(task.status),
        'due': task.due_date,
        'dueComplete': task.due_complete }
    edit_params = set_params(api_params)
    response = requests.put(url_call, data=edit_params)
    return task

def delete_from_tasklist(id):
    url_call = api_url('cardID', id)
    api_params = { 'key':api_key, 'token':api_token }
    response = requests.delete(url_call, params=api_params, timeout=10)
    return get_tasks()


def api_url(board_list_or_card, prop_id=""):
    match board_list_or_card:
        case 'board':
            return 'https://api.trello.com/1/boards/'
        case 'list':
            return 'https://api.trello.com/1/boards/' + board_id + '/lists/'
        case 'listID':
            return 'https://api.trello.com/1/lists/'+ prop_id + '/cards/'
        case 'card':
            return 'https://api.trello.com/1/cards/'
        case 'cardID':
            return 'https://api.trello.com/1/cards/' + prop_id + '/'

def list_id(status):
    match status:
        case 'Not Started':
            return not_started_listid
        case 'In Progress':
            return in_progress_listid
        case 'Complete':
            return complete_listid

def set_params(new_params):
    key_and_token = { 'key':api_key, 'token':api_token }
    params = key_and_token.copy()
    params.update(new_params)
    return params