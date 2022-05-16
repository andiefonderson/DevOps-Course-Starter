import pytest, datetime
from todo_app.view_model import *
from todo_app.data.Item import *

def test_return_items():
    items = dummy_items()
    model = ViewModel(items)
    assert model.items[0].name == 'Test items'

def test_filtered_items():
    items = dummy_items()
    model = ViewModel(items)
    assert model.not_started[0] == items[0]
    assert model.in_progress[0] == items[1]
    assert model.complete[0] == items[2]

def test_hide_completed_items():
    items = dummy_items()
    multi_complete_items = dummy_items_with_more_complete_tasks()
    model = ViewModel(items)
    more_complete_model = ViewModel(multi_complete_items)
    assert model.should_show_all_done_items == True
    assert more_complete_model.should_show_all_done_items == False
    assert model.recent_done_items == [ items[2] ]
    assert model.older_done_items == [ items[3] ]
    assert more_complete_model.older_done_items == [ multi_complete_items[1], multi_complete_items[2], multi_complete_items[3], multi_complete_items[4], multi_complete_items[5], multi_complete_items[6] ]

def dummy_items():
    return [
        Item(1, 'Test items', 'Not Started', False, '', "2022-02-24T13:56:02.920Z"),
        Item(2, 'Make this work', 'In Progress', False, '', "2022-02-24T13:56:02.920Z"),
        Item(3, 'Return items', 'Complete', True, '', datetime.today().strftime("%Y-%m-%dT00:00:00.000Z")),
        Item(4, 'Complete task', 'Complete', True, '', "2022-02-24T13:56:02.920Z")
    ]

def dummy_items_with_more_complete_tasks():
    return [
        Item(1, 'New task', 'Not Started', False, '', "2022-02-24T13:56:02.920Z"),
        Item(2, 'Completed task', 'Complete', True, '', "2022-02-24T13:56:02.920Z"),
        Item(3, 'Another completed task', 'Complete', True, '', "2022-02-24T13:56:02.920Z"),
        Item(4, 'Yet another complete task', 'Complete', True, '', "2022-02-24T13:56:02.920Z"),
        Item(5, 'Testing', 'Complete', True, '', "2022-02-24T13:56:02.920Z"),
        Item(6, 'Test test', 'Complete', True, '', "2022-02-24T13:56:02.920Z"),
        Item(7, 'What? Another test??', 'Complete', True, '', "2022-02-24T13:56:02.920Z")
    ]