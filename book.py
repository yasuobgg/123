class BOOK:
    def __init__(self, name, author, year):
        self.name = name
        self.author = author
        self.year = year

    def to_json(self):
        return{
            'name': self.name,
            'author': self.author,
            'year': self.year
        }

