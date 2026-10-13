from UNIT2.lab5.books import book
from UNIT2.lab5.users import user
from UNIT2.lab5.library import library

book1 = book("1","OPP Fundamentals", "Jhon L", "Cocomelon")
book2 = book("2","OPP Fundamentals2", "Jhon L2", "Cocomelon2")

user1 = user("1", "Jaime", "1305")

library = library()
library.add_books(book1)
library.add_books(book2)
library.add_users(user1)

library.show_list_books()
library.show_list_users()