'''
ToDo:

Fase 1
- Base Classes ✔
- Basic Data Storage ✔
- Basic User Interface ✔

Fase 2
- Able to list all books ✔
- Able to view the information of a book ✔
- Adding books ✔
- Removing books ✔

Fase 3
- Account creation ✔
- Account login ✔
- Account permission checks ✔
- Restrict book editing to libarian

Fase 4
- View loans
- Create loans
- Remove loans (libarian only)

Fase 5
- Finish everything
'''

import typing # For type annotation
import sqlite3
import json
import os
import re #RegEx


# Simple function to clear the console window
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Person:
    username: str
    password: str
    
    givenName: str
    surname: str
    nameSet: str

    streetAddress: str
    city: str
    zipCode: str

    emailAddress: str
    telephoneNumber = "0000000000"

    permType = "Subscriber"

    def __init__(self, username, password, givenName, surname, streetAddress, city, zipCode, emailAddress, telephoneNumber = "0000000000", nameSet = "Dutch", permType = "Subscriber"):
        self.username = username
        self.password = password

        self.givenName = givenName
        self.surname = surname
        self.nameSet = nameSet

        self.streetAddress = streetAddress
        self.city = city
        self.zipCode = zipCode

        self.emailAddress = emailAddress
        self.telephoneNumber = telephoneNumber

        self.permType = permType

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.username == other.username
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


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
    
    def viewInfo(self, returnFunction):
        print(f"ISBN:       {self.isbn}")
        print(f"Title:      {self.title}")
        print(f"Author:     {self.author}")
        print(f"Country:    {self.country}")
        print(f"Language:   {self.language}")
        print(f"Pages:      {self.pages}")
        print(f"Year:       {self.year}")
        print(f"Website:    {self.link}")
        print(f"Image:      {self.imageLink}")

        print("\nPress return to return the booklist...")
        input()
        returnFunction()


class Catalog:
    books = [] #List of Book

    def __init__(self, booksFromDatastore):
        self.books = booksFromDatastore
    
    def search(self):
        pass

    def advancedSearch(self):
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

    # Krijg de lijst van alle beschikbare boeken
    def getAvailableBooks(self):
        return books


class LoanAdministration:
    loans = [] #List of Loan
    
    def getLoansByUser(self):
        return loans
        

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
    loans = []  #List of loans

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

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                username	    TEXT UNIQUE,
                password	    TEXT,
                givenName	    TEXT,
                surname	        TEXT,
                nameSet	        TEXT,
                streetAddress	TEXT,
                city	        TEXT,
                zipCode	        TEXT,
                emailAddress	TEXT,
                telephoneNumber	TEXT,
                permType    	TEXT
            );
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS Loans (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                book	INTEGER,
                user	INTEGER,

                FOREIGN KEY(user) REFERENCES Users(id),
                FOREIGN KEY(book) REFERENCES Books(isbn)
            );
        ''')

        self.db.commit()

        self.books = self.getBooks()
        self.persons = self.getPersons()
        
    def __del__(self):
        self.db.close()

    def getBooks(self):
        books = []

        for row in self.db.execute('SELECT * FROM Books'):
            books.append(Book(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        return books

    def getPersons(self):
        persons = []

        for row in self.db.execute('SELECT * FROM Users'):
            persons.append(Person(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

        return persons

    def getLoans(self):
        loans = []
        
        for row in self.db.execute('SELECT * FROM Loans'):
            loans.append(LoanItem(row[1], row[2], row[3]))

        return loans
    '''
        Saves an instance of a book class to the Database
        Checks for duplicates
    '''
    def addBook(self, book: Book):
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
    def deleteBook(self, book: Book):
        self.cur.execute('DELETE FROM Books WHERE isbn = ?;', (str(book.isbn)))

        self.db.commit()

        self.books.remove(book)

    '''
        Saves an instance of a person class to the Database
        Checks for duplicates
    '''
    def addPerson(self, person: Person):
        if not person in self.persons:
            self.cur.execute('''
                INSERT INTO Users (username, password, givenName, surname, nameSet, streetAddress, city, zipCode, emailAddress, telephoneNumber, permType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            ''', (person.username, person.password, person.givenName, person.surname, person.nameSet, person.streetAddress, person.city, person.zipCode, person.emailAddress, person.telephoneNumber, person.permType))

            self.db.commit()

            self.persons.append(person)
            return True
        else:
            return False

    def usernameInUse(self, username) -> bool:
        return self.getPersonByUsername(username) != None

    def getPersonByUsername(self, username) -> Person:
        for person in self.persons:
            if person.username == username:
                return person
        return None



'''
    Globals
'''
dataStore = DataStore() #DataStore
books = dataStore.getBooks() #List of Book

catalog = Catalog(books)
loans = LoanAdministration()



'''
    UI Classes
'''
class Menu:
    menuOptions = []

    '''
        Takes in an array of tuples containing:
        ("Option Name", CallBack Function, Option parameter for callback)
    '''
    def __init__(self, menuOptions: typing.List[typing.Tuple[str, typing.Callable, typing.Any]]):
        self.menuOptions = menuOptions
        self.render()

    def render(self):
        i = 0
        for menuOption in self.menuOptions:
            print(f'{i}: {menuOption[0]}')
            i = i+1

        print("\nSelect an option by entering it's number and pressing return.")
        selectedIndex = input()

        print("\033[A                             \033[A") #Remove user input from terminal
        
        selectedIndex = int(selectedIndex) if selectedIndex.isdigit() else None
        if selectedIndex != None:
            if selectedIndex < len(self.menuOptions):
                print("\n")
                
                if len(self.menuOptions[selectedIndex]) < 3:
                    self.menuOptions[selectedIndex][1]() # Run the callback of the menu option
                else:
                    self.menuOptions[selectedIndex][1](self.menuOptions[selectedIndex][2]) # Run the callback of the menu option with the arg set in it's option
            else:
                print("The input isn't a valid option!\n\n")
                self.render()
        else:
            print("The input isn't a number!\n\n")
            self.render()


class View:
    title = ""
    subTitle = ""

    permLevel = ""

    def __init__(self, title, subTitle = "", permLevel = "user"):
        self.title = title
        self.subTitle = subTitle
        self.permLevel = permLevel

        self.render()

    def render(self):
        cls()
        self.drawTitleBar()
        pass

    def drawTitleBar(self):
        if self.subTitle != "":
            print(f'========== {self.title} - {self.subTitle} ==========')
        else:
            print(f'========== {self.title} ==========')
        print()


class MainScreen(View):
    currentUser: Person = None

    def setCurrentUser(self, user):
        self.currentUser = user

    def render(self):
        super().render()

        if self.currentUser != None:
            print(f"Welcome {self.currentUser.givenName} {self.currentUser.surname} ({self.currentUser.permType}) to the Public Library System. ")
        else:
            print("Welcome to the Public Library System.")
        print()

        menuOptions = None

        if self.currentUser == None:
            menuOptions = [
                ("Register Account", self.registerAccount),
                ("Logon", self.logIn ),
                ("Debug Menu", self.debug, "test"),
                ("Exit", exit),
            ]
        else:
            menuOptions = [
                ("List book titles", self.drawBookTitles),
                ("Debug Menu", self.debug, "test"),
                ("Exit", exit),
            ]
            if(self.currentUser.permType == "Libarian"):
                menuOptions.insert(0, ("Add Book", self.addBook))
                menuOptions.insert(1, ("Import Books", self.importBooks))
                menuOptions.insert(2, ("Import Users", self.importUsers))
                menuOptions.insert(3, ("Create Backup", self.createBackup))

        Menu(menuOptions)

    def drawBookTitles(self):
        bookMenuOptions = []
        
        for book in catalog.getAvailableBooks():
            bookMenuOptions.append((book.title, book.viewInfo, self.drawBookTitles))
            
        bookMenuOptions.append(("Return to Main Menu", self.render))
        Menu(bookMenuOptions)
        
    def registerAccount(self):
        AccountCreation("Account Creation")
        
    def logIn(self):
        Login("Logon", self)

    def debug(self, arg):
        cls()
        print(f"It works! {arg}")

    def addBook(self):
        print("Not implemented!")

    def importBooks(self):
        print("Not implemented!")

    def importUsers(self):
        print("Not implemented!")

    def createBackup(self):
        print("Not implemented!")


class AccountCreation(View):
    def render(self):
        super().render()

        print("Please fill in your username:")
        enteredUsername: str = input()
        while enteredUsername == "":
            print("\nUsername can not be empty!")
            print("Please fill in your username:")
            enteredUsername = input()
        while dataStore.usernameInUse(enteredUsername):
            print("\nUsername already in use!")
            print("Please fill in your username:")
            enteredUsername = input()
            

        print("Please fill in your password:")
        enteredPassword: str = input()
        print("\033[A                             \033[A") #Remove user input from terminal
        while enteredPassword == "":
            print("\nPassword can not be empty!")
            print("Please fill  your password:")
            enteredPassword = input()
            print("\033[A                             \033[A") #Remove user input from terminal


        print("Please fill in your first name: ")
        enteredGivenName: str = input()
        while enteredGivenName == "":
            print("\nYour first name can not be empty!")
            print("Please fill in your first name: ")
            enteredGivenName = input()


        print("Please fill in your surname: ")
        enteredSurname: str = input()
        while enteredSurname == "":
            print("\nYour surname can not be empty!")
            print("Please fill in your surname: ")
            enteredSurname = input()


        print("Please fill in your street adress: ")
        enteredStreetAddress: str = input()
        while enteredStreetAddress == "":
            print("\nYour street adress can not be empty!")
            print("Please fill in your street adress: ")
            enteredStreetAddress = input()
        

        print("Please fill in your city: ")
        enteredCity: str = input()
        while enteredCity == "":
            print("\n Your city can not be empty!")
            print("Please fill in your city: ")
            enteredCity = input()


        print("Please fill in your zip code: ")
        enteredZipCode: str = input()
        while enteredZipCode == "":
            print("\nYour zip code can not be empty!")
            print("Please fill in your zip code: ")
            enteredZipCode = input()


        print("Please enter your email adress: ")
        enteredEmailAddress: str = input()
        while not self.isEmailValid(enteredEmailAddress):
            print("\nThis email adress is not valid!")
            print("Please fill in your email adress:")
            enteredEmailAddress = input()


        print("Please fill in your phone number (optional): ")
        enteredTelephoneNumber: str = input()
        
        while not self.isPhoneValid(enteredTelephoneNumber) and enteredTelephoneNumber != "":
            print("\nThis phone number is not valid!")
            print("Please fill in your phone number: ")
            enteredTelephoneNumber = input()
            
        person = Person(enteredUsername, enteredPassword, enteredGivenName, enteredSurname, enteredStreetAddress, enteredCity, enteredZipCode, enteredEmailAddress, enteredTelephoneNumber, "Dutch")

        dataStore.addPerson(person)

    def isEmailValid(self, email) -> bool:
        pattern = re.compile("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])", re.IGNORECASE)
        return pattern.match(email) is not None

    def isPhoneValid(self, number) -> bool: 
        pattern = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
        return pattern.match(number) is not None


class Login(View):
    mainView: MainScreen

    def __init__(self, title, mainView, subTitle = "", permLevel = "Subscriber"):
        self.mainView = mainView
        super().__init__(title, subTitle=subTitle, permLevel=permLevel)

    def render(self):
        super().render()
        
        print("Please fill in your username:")
        enteredUsername: str = input()
        while enteredUsername == "":
            print("\nUsername can not be empty!")
            print("Please fill in your username:")
            enteredUsername = input()
        while not dataStore.usernameInUse(enteredUsername):
            print("\nUnknown username!")
            print("Please fill in your username:")
            enteredUsername = input()
            
        person = dataStore.getPersonByUsername(enteredUsername)

        print("Please fill in your password:")
        enteredPassword: str = input()
        print("\033[A                             \033[A") #Remove user input from terminal
        while enteredPassword == "":
            print("\nPassword can not be empty!")
            print("Please fill  your password:")
            enteredPassword = input()
            print("\033[A                             \033[A") #Remove user input from terminal

        triesLeft = 3
        while enteredPassword != person.password and triesLeft > 0:
            print(f"\nPassword doesn't match! ({triesLeft} attempts left)")
            print("Please fill  your password:")
            enteredPassword = input()
            print("\033[A                             \033[A") 
            triesLeft = triesLeft - 1

        if triesLeft <= 0:
            print("Max login attempts reached, quitting...")
            exit()

        # Set the current user and return to the main view
        self.mainView.setCurrentUser(person)
        self.mainView.render()


class AddBook(View):
    def render():
        super().render()

        

'''
    Initialize Main UI
'''
mainScreen = MainScreen("Main Menu")


'''
    Example adding book to DB
    
    cat = Catalog()
    cat.addBook(9789020415605, 'Moby-Dick', 'Herman Melville', 'Netherlands', 'English', 640, 2008,'https://www.bol.com/nl/f/moby-dick/9200000079749152/', 'https://media.s-bol.com/mZZYJDPj0jkr/539x840.jpg')
    cat.addBook(9789044643947, 'Het gouden ei', 'Tim Krabbé', 'Netherlands', 'Dutch', 104, 2019, 'https://www.bol.com/nl/f/gouden-ei/9200000079749088/', 'https://media.s-bol.com/J6Q0MLXyWXxg/525x840.jpg')
'''
        

print()