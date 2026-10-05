class book:
    def __init__(self, id_book, title, author, editorial):
        self.id_book = id_book
        self.title = title
        self.author = author 
        self.editorial = editorial

    def show_book_info(self):
        return f"{self.id_book} - {self.title} - {self.author} - {self.editorial}"