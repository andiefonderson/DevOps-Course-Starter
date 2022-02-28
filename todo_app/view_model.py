from datetime import date, datetime

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items
    
    @property
    def not_started(self):
        return self.filter_list_by_status('Not Started')
    
    @property
    def in_progress(self):
        return self.filter_list_by_status('In Progress')

    @property
    def complete(self):
        return self.filter_list_by_status('Complete')
    
    @property
    def should_show_all_done_items(self):
        return len(self.complete) < 5

    @property
    def recent_done_items(self):
        done_items = self.complete
        recently_done = []
        for item in done_items:
            last_mod_date = datetime.strptime(item.last_modified_date[0:-14],"%Y-%m-%d").date()
            if last_mod_date == date.today():
                recently_done.append(item)
        return recently_done
    
    @property
    def older_done_items(self):
        done_items = self.complete
        older_tasks = []
        for item in done_items:
            last_mod_date = datetime.strptime(item.last_modified_date[0:-14],"%Y-%m-%d").date()
            if last_mod_date != date.today():
                older_tasks.append(item)
        return older_tasks
    
    def filter_list_by_status(self, status):
        list = []
        for item in self._items:
            if(item.status == status):
                list.append(item)
        return list