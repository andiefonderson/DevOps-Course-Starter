from datetime import datetime
import os, requests

from todo_app.data.Item import Item



def get_tasks():
    api_params = {"fields":"name", 
        "cards":"all", 
        "card_fields":"name,desc,closed,due,dueComplete,dateLastActivity"}
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


def get_task(id):
    tasks = get_tasks()
    for task in tasks:
        if id == task.id:
            return task

def create_task(task_name, task_due_date="", task_notes=""):
    api_params = { 'idList': list_id('Not Started'),
        'name': task_name,
        'due': task_due_date,
        'desc': task_notes }
    create_params = set_params(api_params)
    response = requests.post(api_url('card'), data=create_params).json()
    return response

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
    api_params = set_params('')
    response = requests.delete(url_call, params=api_params, timeout=10)
    return get_tasks()


def api_url(board_list_or_card, prop_id=""):
    board_id = os.getenv('TRELLO_BOARD_ID')
    match board_list_or_card:
        case 'board':
            return 'https://api.trello.com/1/boards/'
        case 'list':
            return f'https://api.trello.com/1/boards/{board_id}/lists/'
        case 'listID':
            return f'https://api.trello.com/1/lists/{prop_id}/cards/'
        case 'card':
            return 'https://api.trello.com/1/cards/'
        case 'cardID':
            return f'https://api.trello.com/1/cards/{prop_id}/'

def list_id(status):
    not_started_listid = os.getenv('NOT_STARTED_LIST_ID')
    in_progress_listid = os.getenv('IN_PROGRESS_LIST_ID')
    complete_listid = os.getenv('COMPLETE_LIST_ID')
    match status:
        case 'Not Started':
            return not_started_listid
        case 'In Progress':
            return in_progress_listid
        case 'Complete':
            return complete_listid

def set_params(new_params):
    api_key = os.getenv('TRELLO_KEY')
    api_token = os.getenv('TRELLO_TOKEN')

    key_and_token = { 'key':api_key, 'token':api_token }
    
    if new_params == '':
        return key_and_token
    else:
        params = key_and_token.copy()
        params.update(new_params)
        return params