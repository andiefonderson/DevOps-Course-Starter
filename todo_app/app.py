from flask import Flask, render_template, redirect, request

from todo_app.data.api_caller import *
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    sorted_list = sorted(get_tasks(), key=lambda item:item.status, reverse=True)
    return render_template("index.html", to_do_items=sorted_list)

@app.route('/', methods=['POST'])
def add_to_do():
    create_task(request.form.get('to-do-title'), request.form.get('to-do-notes'))
    return redirect('/')

@app.route('/task/<id>')
def view_to_do_item(id):
    task = get_task(id)
    return render_template("task.html", task=task)

@app.route('/task/<id>', methods=['POST'])
def amend_item(id):
    old_task = get_task(id)
    amended_status = request.form.get('task-status')
    amended_title = request.form.get('task-title')
    amended_notes = request.form.get('task-notes')
    amended_due_date = request.form.get('task-due-date')
    print(amended_due_date)
    amended_due_complete = True if amended_status == "Complete" else False
    if amended_due_date == "":
        amended_due_date = old_task.due_date
    task = Item(id, amended_title, amended_status, amended_due_complete, amended_due_date, amended_notes)
    edit_task(task)
    return redirect('/task/' + id)

@app.route('/delete/<id>')
def view_delete_item(id):
    task = get_task(id)
    return render_template("deletetask.html", task=task)

@app.route('/delete/<id>', methods=['POST'])
def delete_task(id):
    delete_from_tasklist(id)
    return redirect('/')