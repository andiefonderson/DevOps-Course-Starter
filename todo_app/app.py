from datetime import date
from flask import Flask, render_template, redirect, request
import gunicorn

from todo_app.data.trello_items import *
import todo_app.flask_config
from todo_app.view_model import ViewModel

def create_app():
    app = Flask(__name__)  
    app.config.from_object(todo_app.flask_config.Config())


    @app.route('/')
    def index():
        sorted_list = get_tasks()
        item_view_model = ViewModel(sorted_list)
        return render_template("index.html", view_model=item_view_model)

    @app.route('/<status>')
    def filtered_index(status):
        model = ViewModel(get_tasks())
        filter_list = []
        match(status):
            case 'not-started':
                filter_list = model.not_started
            case 'in-progress':
                filter_list = model.in_progress
            case 'complete':
                filter_list = model.filter_list_by_status('Complete')
        filtered_model = ViewModel(filter_list)
        return render_template("index.html", view_model=filtered_model)

    @app.route('/', methods=['POST'])
    def add_to_do():
        due_date = request.form.get('task-due-date')
        if due_date != "":
            due_date = datetime.strptime(request.form.get('task-due-date'), "%d/%m/%Y")
        create_task(request.form.get('to-do-title'), due_date, request.form.get('to-do-notes'))
        return redirect('/')

    @app.route('/<status>', methods=['POST'])
    def add_to_do_from_filtered_tasks(status):
        add_to_do()
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
        date = request.form.get('task-due-date')
        amended_due_complete = "true" if amended_status == "Complete" else "false"
        amended_due_date = datetime.strptime(date, "%d/%m/%Y") if date != "" else ""
        
        task = Item(id, amended_title, amended_status, amended_due_complete, amended_due_date, None, amended_notes)
        edit_task(task)
        return redirect('/task/' + id)

    @app.route('/delete/<id>')
    def view_delete_item(id):
        task = get_task(id)
        if task != None:
            return render_template("deletetask.html", task=task)
        else:
            return redirect('/')

    @app.route('/delete/<id>', methods=['POST'])
    def delete_task(id):
        if request.form.get('delete-task-button'):
            delete_from_tasklist(id)
        return redirect('/')

    return app