from flask import json, request
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
        "card_fields":"name"}
    response = requests.get(api_url, params=auth_string)
    list_cards = json.loads(response.text)
    for list in list_cards:
        print("Status: " + list['name'])
        for card in list['cards']:
            print("Task: " + card['name'])


get_tasks()