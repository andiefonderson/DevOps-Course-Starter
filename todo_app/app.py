from flask import Flask, render_template, redirect, request

from todo_app.data.session_items import *
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():    
    list = get_items()
    return render_template("index.html", to_do_items=list)

@app.route('/', methods=['POST'])
def add_to_do():
    add_item(request.form.get('to-do-title'))
    return redirect('/')

@app.route('/task/<id>')
def view_to_do_item(id):
    task = get_item(id)
    return render_template("task.html", task=task)

@app.route('/task/<id>', methods=['POST'])
def amend_item(id):
    amended_status = request.form.get('task-status')
    amended_title = request.form.get('task-title')
    task = { 'id': int(id), 'status': amended_status, 'title': amended_title }
    save_item(task)
    return redirect('/')

