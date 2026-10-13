from books import book
from users import user


class library:
    def __init__(self):
        self.users = []
        self.books = []

    def add_users(self, user):
        self.users.append(user)

    def add_books(self, book):
            self.books.append(book)

    def show_list_books(self):
        for m in self.books:
            print (book.show_book_info(m))

    def show_list_users(self):
        for m in self.users:
            print (user.show_user_info(m))
         

