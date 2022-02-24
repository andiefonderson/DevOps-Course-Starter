import os, requests

def create_board(board_name):
    url = 'https://api.trello.com/1/boards/'
    api_params = params({ 'name': board_name })
    response = requests.post(url, api_params).json()
    print(f'Board "{board_name}" created')
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
    list_ids = []
    for list in response:
        change_list_name(list['id'], list['name'])

def change_list_name(list_id, list_name):
    url = f'https://api.trello.com/1/lists/{list_id}'
    match list_name:
        case 'To Do':
            new_list_name = 'Not Started'
        case 'Doing':
            new_list_name = 'In Progress'
        case 'Done':
            new_list_name = 'Complete'
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

new_board_id = create_board('test to be deleted')
delete_board(new_board_id)