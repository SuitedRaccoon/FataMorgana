class Book:
    def __init__(self, id, title, author, genre, year):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.year = year

    def __repr__(self):
        return f"<Book: {self.title} by {self.author}>"
