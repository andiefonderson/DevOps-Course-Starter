class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items
    
    @property
    def not_started(self):
        return self.filter_list('Not Started')
    
    @property
    def in_progress(self):
        return self.filter_list('In Progress')

    @property
    def complete(self):
        return self.filter_list('Complete')
    
    def filter_list(self, status):
        list = []
        for item in self._items:
            if(item.status == status):
                list.append(item)
        return list