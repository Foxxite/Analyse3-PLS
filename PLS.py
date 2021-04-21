'''
ToDo:

Fase 1
- Base Classes ✔
- Basic Data Storage ✔
- Basic User Interface

Fase 2
- Able to list all books
- Able to view the information of a book
- Adding books ✔
- Removing books ✔

Fase 3
- Account creation
- Account permission
- Restrict book editing to libarian

Fase 4
- View loons
- Create loons
- Remove loons

Fase 5
- Finish everything
'''

import sqlite3
import json

class Person:
    username = "" #string

    givenName = "" #string
    surname = "" #string
    nameSet = "" #string

    streetAddress = "" #string
    city = "" #string
    zipCode = "" #string

    emailAddress = "" #string
    telephoneNumber = 0000000000 #int 10 digits

    def __init__(self, username, givenName, surname, streetAddress, city, zipCode, emailAddress, telephoneNumber = 0000000000, nameSet = "Dutch"):
        self.username = username

        self.givenName = givenName
        self.surname = surname
        self.nameSet = nameSet

        self.streetAddress = streetAddress
        self.city = city
        self.zipCode = zipCode

        self.emailAddress = emailAddress
        self.telephoneNumber = telephoneNumber

class Libearian(Person):
    pass

class Subscriber(Person):
    pass

class Book:
    isbn = 0000000000000 #int 13 digits

    title = '' #string
    author = '' #string

    country = '' #string
    language = '' #string

    pages = 0 #int
    year = 0000 #int
    link = '' #string
    imageLink = '' #string

    def __init__(self, isbn, title, author, country, language, pages, year, link, imageLink):
        self.isbn = isbn

        self.title = title 
        self.author = author

        self.country = country
        self.language = language

        self.pages = pages
        self.year = year
        self.link = link
        self.imageLink = imageLink

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.isbn == other.isbn
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Catalog:
    books = [] #List of Book

    def __init__(self, booksFromDatastore):
        self.books = booksFromDatastore
    
    def search():
        pass

    def advancedSearch():
        pass
    
    '''
        Adding a book

        1) Take all information of the book as parameters
        2) Create instance of Book class
        3) Write book to database using the datastore global
        4) Append book to the internal book list
    '''
    def addBook(self, isbn, title, author, country, language, pages, year, link, imageLink):
        book = Book(isbn, title, author, country, language, pages, year, link, imageLink)
        dataStore.addBook(book)
        books.append(book)
        
    #verwijder boek
    def removeBook(self, isbn):
        book = None
        for b in books:
            if b.isbn == isbn:
                book = b
                break

        if book != None:
            books.remove(book)
            dataStore.deleteBook(book)

    #krijg het boek
    def getAvailableBooks():
        pass

class LoanAdministration:
    loans = [] #List of Loan
    
    def getLoansByUsers(self):
        pass
    
    def addLoan(self):
        pass
    
    def removeLoan(self):
        pass

class LoanItem():
    book = None #Book
    person = None #Person

    pass


class DataStore:
    books = [] #List of Books
    persons = [] #List of Persons

    db = None #SQLite Connection
    cur = None #SQLite Cursor

    def __init__(self):
        self.db = sqlite3.connect('database.db')
        self.cur = self.db.cursor()

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                isbn        INTEGER,
                title       TEXT,
                author      TEXT,
                country     TEXT,
                language    TEXT,
                pages	    INTEGER DEFAULT 0,
                year	    INTEGER DEFAULT 0000,
                link	    TEXT,
                imgLink	    TEXT,

                PRIMARY KEY(isbn)
            )
        ''')
        self.db.commit()

        self.books = self.getBooks()
        
    def __del__(self):
        self.db.close()

    def getBooks(self):
        books = []

        for row in self.db.execute('SELECT * FROM Books'):
            books.append(Book(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        return books

    '''
        Saves an instance of a book class to the Database
        Checks for duplicates
    '''
    def addBook(self, book):
        if not book in self.books:
            self.cur.execute('''
                INSERT INTO Books (isbn, title, author, country, language, pages, year, link, imgLink) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', (book.isbn, book.title, book.author, book.country, book.language, book.pages, book.year, book.link, book.imageLink))

            self.db.commit()

            self.books.append(book)
            return True
        else:
            return False

    '''
        Deletes a book from the Database by ISBN
    '''
    def deleteBook(self, book):
        self.cur.execute('DELETE FROM Books WHERE isbn = ?;', (str(book.isbn)))

        self.db.commit()

        self.books.remove(book)

dataStore = DataStore() #DataStore
books = dataStore.getBooks() #List of Book

catalog = Catalog(books) 
catalog.removeBook(1)

'''
    Example adding book to DB
    
    cat = Catalog()
    cat.addBook(9789020415605, 'Moby-Dick', 'Herman Melville', 'Netherlands', 'English', 640, 2008,'https://www.bol.com/nl/f/moby-dick/9200000079749152/', 'https://media.s-bol.com/mZZYJDPj0jkr/539x840.jpg')
    cat.addBook(9789044643947, 'Het gouden ei', 'Tim Krabbé', 'Netherlands', 'Dutch', 104, 2019, 'https://www.bol.com/nl/f/gouden-ei/9200000079749088/', 'https://media.s-bol.com/J6Q0MLXyWXxg/525x840.jpg')
'''
        

print()