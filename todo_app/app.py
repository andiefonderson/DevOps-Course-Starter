from flask import Flask, render_template, redirect, request

from todo_app.data.session_items import *
from todo_app.data.api_caller import get_task, get_tasks
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():    
    # list = sorted(get_items(), key=lambda item:item['status'], reverse=True)
    sorted_list = sorted(get_tasks(), key=lambda item:item['status'], reverse=True)
    return render_template("index.html", to_do_items=sorted_list)

@app.route('/', methods=['POST'])
def add_to_do():
    add_item(request.form.get('to-do-title'), request.form.get('to-do-notes'))
    return redirect('/')

@app.route('/task/<id>')
def view_to_do_item(id):
    task = get_task(id)
    return render_template("task.html", task=task)

@app.route('/task/<id>', methods=['POST'])
def amend_item(id):
    amended_status = request.form.get('task-status')
    amended_title = request.form.get('task-title')
    amended_notes = request.form.get('task-notes')
    task = { 'id': int(id), 'status': amended_status, 'title': amended_title, 'notes': amended_notes }
    save_item(task)
    return redirect('/')

@app.route('/delete/<id>')
def view_delete_item(id):
    task = get_item(id)
    return render_template("deletetask.html", task=task)

@app.route('/delete/<id>', methods=['POST'])
def delete_task(id):
    if request.form.get('delete-task-button'):
        delete_item(id)

    return redirect('/')