from datetime import datetime

class Item:
    def __init__(self, id, name, status, due_complete, due_date, last_modified_date, notes = ''):
        self.id = id
        self.name = name
        self.status = status
        self.due_complete = due_complete
        self.due_date = due_date
        self.last_modified_date = last_modified_date
        self.notes = notes
        if self.due_date != None:
            try:
                simple_date = datetime.strptime(self.due_date[0:-8],"%Y-%m-%dT%H:%M").date()
                self.simplified_date = simple_date.strftime("%d/%m/%Y")
            except:
                self.simplified_date = self.due_date
        else:
            self.simplified_date = ""

    def __getitem__(self, id):
        return self.id

    @classmethod
    def from_trello_card(cls, card, status):
        return cls(card['id'], card['name'], status, card['dueComplete'], card['due'], card['dateLastActivity'], card['desc'])