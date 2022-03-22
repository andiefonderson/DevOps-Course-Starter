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
        if self.should_show_all_done_items:
            return self.filter_list_by_status('Complete')
        else:
            return self.recent_done_items
    
    @property
    def should_show_all_done_items(self):
        return len(self.filter_list_by_status('Complete')) < 5

    @property
    def recent_done_items(self):
        done_items = self.filter_list_by_status('Complete')
        recently_done = []
        for item in done_items:
            last_mod_date = datetime.strptime(item.last_modified_date[0:-14],"%Y-%m-%d").date()
            if last_mod_date == date.today():
                recently_done.append(item)
        return recently_done
    
    @property
    def older_done_items(self):
        done_items = self.filter_list_by_status('Complete')
        older_tasks = []
        for item in done_items:
            last_mod_date = datetime.strptime(item.last_modified_date[0:-14],"%Y-%m-%d").date()
            if last_mod_date != date.today():
                older_tasks.append(item)
        return older_tasks
    
    @property
    def no_items_in_model(self):
        return len(self._items) == 0
    
    @property
    def no_items_in_not_started(self):
        return len(self.not_started) == 0
    
    @property
    def no_items_in_in_progress(self):
        return len(self.in_progress) == 0
    
    @property
    def no_items_in_complete(self):
        return len(self.filter_list_by_status('Complete')) == 0

    def filter_list_by_status(self, status):
        list = []
        for item in self._items:
            if(item.status == status):
                list.append(item)
        return list