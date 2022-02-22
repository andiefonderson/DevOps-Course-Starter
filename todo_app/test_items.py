import pytest
from view_model import *
from data.Item import *

def test_return_items():
    items = [
        Item(1, 'Test items', 'Not Started', False, '' ),
        Item(2, 'Make this work', 'In Progress', False, '' ),
        Item(3, 'Return items', 'Complete', True, '')
    ]
    model = ViewModel(items)
    assert model.items[0].name == 'Test items'

def test_filtered_items():
    items = [
        Item(1, 'Test items', 'Not Started', False, '' ),
        Item(2, 'Make this work', 'In Progress', False, '' ),
        Item(3, 'Return items', 'Complete', True, '')
    ]
    model = ViewModel(items)
    assert model.not_started[0] == items[0]
    assert model.in_progress[0] == items[1]
    assert model.complete[0] == items[2]