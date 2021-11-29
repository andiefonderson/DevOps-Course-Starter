from flask import Flask, render_template, redirect, request
# from session_items import *

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