# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.10+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

The project is set up to integrate with a Trello board. In the `.env`, you will need to enter in your API key and token as well as the board ID. You can find your API key and token on Trello's dedicated [Developer API Keys](https://trello.com/app-key) webpage.

When adding in the API key and token into the `.env` file, enter it into the file as follows:
```
TRELLO_KEY= (enter key here)
TRELLO_TOKEN= "(enter token here)"
```

You will then need to enter the board ID of a to-do list as well as the IDs of the lists. When setting up the board for the lists, the app has been configured to have 'Not Started, 'In Progress', and 'Complete' lists as the task status. To make the filters work properly, please make sure the list titles match these statuses.

When the board has been set up, you can use the Trello API to find the IDs of the board and lists. The easiest API requests to use for this would be the '[Get All Boards You're a Member To](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#getting-our-member-s-boards)' and, using the board ID for it, the '[Get Lists on a Board](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-lists-get)'. Once you have gotten them, input their values into the `.env` file as follows:
```
TRELLO_BOARD_ID= (enter board ID here)

NOT_STARTED_LIST_ID= (enter 'Not Started' list ID here)
IN_PROGRESS_LIST_ID= (enter 'In Progress' list ID here)
COMPLETE_LIST_ID=(enter 'Complete' list ID here)
```

The unit tests use pytest. For more information on pytest, visit the [information page on PyPi](https://pypi.org/project/pytest/).

If running this through Visual Studio Code, install the Python and Python Test Explorer for Visual Studio Code extensions. You will then be able to use the 'Testing' tab to run your tests.
Alternatively, you can run the tests by entering `poetry run pytest` as a command in the terminal.

The tests also use Selenium through Firefox. You will need to have Firefox (version 97.0.1 or higher) installed to ensure these tests will work.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
