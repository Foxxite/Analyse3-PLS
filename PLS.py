class Person:
    username = ""

    givenName = ""
    surname = ""
    nameSet = ""

    streetAddress = ""
    city = ""
    zipCode = ""

    emailAddress = ""
    telephoneNumber = 0000000000

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
    isbn = 0

    title = ''
    author = ''

    country = ''
    language = ''

    pages = 0
    year = 0000
    link = ''
    imageLink = ''

    def _init_(self, isbn,  title, author, country, language, pages, year, link, imageLink):
        self.isbn = isbn

        self.title = title 
        self.author = author

        self.country = country
        self.language = language

        self.pages = pages
        self.year = year
        self.link = link
        self.imageLink = imageLink

class Catalog:
    books = []

    def _init_():
        pass
    
    def search():
        pass

    def advancedSearch():
        pass

    def addBook():
        pass

    def removeBook():
        pass

    def getAvailableBooks():
        pass

class LoanAdministration:
    loans = []
    
    def getLoansByUsers(self):
        pass
    
    def addLoan(self):
        pass
    
    def removeLoan(self):
        pass

class LoanItem():  # <-- call class book and person
    pass