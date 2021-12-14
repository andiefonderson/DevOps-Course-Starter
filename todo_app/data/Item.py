class Item:
    def __init__(self, id, name, status, due_complete, due_date, notes = 'To Do'):
        self.id = id
        self.name = name
        self.status = status
        self.due_complete = due_complete
        self.due_date = due_date
        self.notes = notes

    def __getitem__(self, id):
        return self.id

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'], card['dueComplete'], card['due'], card['desc'])