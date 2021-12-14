class Item:
    def __init__(self, id, name, status, notes = 'To Do'):
        self.id = id
        self.name = name
        self.status = status
        self.notes = notes

    def __getitem__(self, id):
        return self.id

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'], card['desc'])