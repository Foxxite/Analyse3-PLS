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
- Restrict book editing to Librarian ✔

Fase 4
- View loans ✔
- Create loans ✔
- Remove loans (Librarian only) ✔

Fase 5
- View Account Info ✔
- Delete accounts (Librarian only) ✔
- Delete books (Librarian only) ✔
'''

import typing # For type annotation
import sqlite3

import json
import csv

import os
import re #RegEx
import random


# Simple function to clear the console window
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Person:
    id: int

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
        
        print()

        menuOptions = [
            ("Loan Book", loanAdministration.addLoan, self),
            ("Return to book list", returnFunction)
        ] 
        Menu(menuOptions)


class LoanItem:
    book: Book = None #Book
    user: Person = None #Person

    def __init__(self, user, book):
        self.user = user
        self.book = book


class LoanAdministration:
    loans: typing.List[LoanItem] = [] #List of Loan
    
    def __init__(self, loans):
        self.loans = loans

    def getLoansByUser(self, user):
        loansOfUser = []

        for loan in self.loans:
            if loan.user == user:
                loansOfUser.append(loan)

        return loansOfUser


    def addLoan(self, book):
        loan = LoanItem(currentUser, book)
        dataStore.addLoan(loan)
        self.loans.append(loan)
    
    def removeLoan(self):
        pass


class DataStore:
    books: typing.List[Book] = [] #List of Books
    persons: typing.List[Person] = [] #List of Persons
    loans: typing.List[LoanItem] = []  #List of loans

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
                user	TEXT,

                FOREIGN KEY(user) REFERENCES Users(username),
                FOREIGN KEY(book) REFERENCES Books(isbn)
            );
        ''')

        self.db.commit()

        self.books = self.getBooks()
        self.persons = self.getPersons()
        self.loans = self.getLoans()
        
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
            username = row[1]
            password = row[2]
            givenName = row[3]
            surname = row[4]
            nameSet = row[5]
            streetAddress = row[6]
            city = row[7]
            zipCode = row[8]
            emailAddress = row[9]
            telephoneNumber = row[10]
            permType = row[11]

            persons.append(Person(username, password, givenName, surname, streetAddress, city, zipCode, emailAddress, telephoneNumber, nameSet, permType))

        return persons

    def getLoans(self):
        loans = []
        
        for row in self.db.execute('SELECT * FROM Loans'):
            user = self.getPersonByUsername(row[2])
            book = self.getBookByISBN(row[1])

            loan = LoanItem(user, book)
            loans.append(loan)

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


    def addLoan(self, loan: LoanItem):
        self.cur.execute('''
            INSERT INTO Loans (user, book) VALUES (?, ?);
            ''', (loan.user.username, loan.book.isbn))

        self.db.commit()

        self.loans.append(loan)
        
    
    '''
        Deletes a book from the Database by ISBN
    '''
    def deleteBook(self, book: Book):
        self.cur.execute('DELETE FROM Books WHERE isbn = ?;', (str(book.isbn),))
        self.cur.execute('DELETE FROM Loans WHERE book = ?;', (str(book.isbn),))

        self.db.commit()

        self.books.remove(book)

        global catalog
        catalog = Catalog(self.books)

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

    def getBookByISBN(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def deletePerson(self, person):
        username = (person.username,)

        self.cur.execute('DELETE FROM Users WHERE username = ?;', username)
        self.cur.execute('DELETE FROM Loans WHERE user = ?;', username)

        self.db.commit()

        self.persons.remove(person)


    def deleteLoan(self, loan):
        self.cur.execute('DELETE FROM Loans WHERE user = ? AND book = ?;', (loan.user.username, loan.book.isbn))

        self.db.commit()

        self.loans.remove(loan)

        global loanAdministration
        loanAdministration = LoanAdministration(self.loans)

'''
    Globals
'''
dataStore: DataStore = DataStore() #DataStore
books: typing.List[Book] = dataStore.getBooks() #List of Book

loanAdministration: LoanAdministration = LoanAdministration(dataStore.loans)

currentUser: Person = None

class Catalog:
    books: typing.List[Book] = [] #List of Book

    def __init__(self, booksFromDatastore):
        self.books = booksFromDatastore
    
    def search(self):
        pass

    def advancedSearch(self):
        pass
    

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
        books = []

        for book in self.books:
            isAvailable = True
            
            for loan in loanAdministration.loans:
                if loan.book == book:
                    isAvailable = False
                    break;
            
            if isAvailable:
                books.append(book)

        return books

catalog: Catalog = Catalog(books)

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
    def setCurrentUser(self, user):
        global currentUser
        currentUser = user

    def render(self):
        super().render()

        if currentUser != None:
            print(f"Welcome {currentUser.givenName} {currentUser.surname} ({currentUser.permType}) to the Public Library System. ")
        else:
            print("Welcome to the Public Library System.")
        print()

        menuOptions = None

        if currentUser == None:
            menuOptions = [
                ("Register Account", self.registerAccount),
                ("Logon", self.logIn ),
                ("About", self.about),
                ("Exit", exit),
            ]
        else:
            menuOptions = [
                ("List Book Titles", self.drawBookTitles),
                ("List My Loans", self.listLoans),
                ("View Account Info", self.viewAccountInfo),
                ("About", self.about),
                ("Exit", exit),
            ]
            if(currentUser.permType == "Librarian"):
                menuOptions.insert(0, ("Add Book", self.addBook))
                menuOptions.insert(1, ("Import Books", self.importBooks))
                menuOptions.insert(2, ("Import Users", self.importUsers))
                menuOptions.insert(3, ("Create Backup", self.createBackup))
                menuOptions.insert(4, ("Remove A Loan", self.removeLoans))
                menuOptions.insert(5, ("Delete An Account", self.deleteAccount))
                menuOptions.insert(6, ("Delete A Book", self.deleteBook))

        Menu(menuOptions)

        self.render()

    def drawBookTitles(self):
        bookMenuOptions = []
        
        for book in catalog.getAvailableBooks():
            bookMenuOptions.append((f"{book.title} - {book.author}", book.viewInfo, self.drawBookTitles))
            
        bookMenuOptions.append(("Return to Main Menu", self.render))
        Menu(bookMenuOptions)
        
    def registerAccount(self):
        AccountCreation("Account Creation")
        
    def logIn(self):
        Login("Logon", self)

    def about(self, arg):
        cls()
        print("PLS by 1007284, 0970671, 1008730")
        print("\nPress return to return to the main menu!")
        input()

    def addBook(self):
        AddBook("Adding a book", self)

    def importBooks(self):
        ImportBooks("Importing books from file")

    def importUsers(self):
        ImportUsers("Importing users from file")

    def createBackup(self):
        CreateBackup("Creating Backup")

    def listLoans(self):
        LoanList("My Loans")
    
    def removeLoans(self):
        loanMenuOptions = []
        
        for loan in loanAdministration.loans:
            loanMenuOptions.append((f"{loan.user.givenName} {loan.user.surname} | {loan.book.isbn} {loan.book.title} {loan.book.author}", dataStore.deleteLoan, loan))
            
        loanMenuOptions.append(("Cancel", self.render))
        Menu(loanMenuOptions)

        print("Loan deleted! Press return to return to the main menu!")
        input()

    def viewAccountInfo(self):
        AccountInfo("Account Information")

    def deleteAccount(self):
        AccountDeletion("Account Deletion")

    def deleteBook(self):
        bookMenuOptions = []
        
        for book in catalog.getAvailableBooks():
            bookMenuOptions.append((f"{book.isbn} - {book.title} {book.author}", dataStore.deleteBook, book))
            
        bookMenuOptions.append(("Cancel", self.render))
        Menu(bookMenuOptions)

        print("Book deleted! Press return to return to the main menu!")
        input()

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
            print("Please fill in your password:")
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


class AccountInfo(View):
    def render(self):
        super().render()
        
        print(f"Username: {currentUser.username}")
        print(f"Given Name: {currentUser.givenName}")
        print(f"Surname: {currentUser.surname}")
        print(f"Street Address: {currentUser.streetAddress}")
        print(f"City: {currentUser.city}")
        print(f"Zip Code: {currentUser.zipCode}")
        print(f"Email Address: {currentUser.emailAddress}")
        print(f"Telephone number: {currentUser.telephoneNumber}")
        print("")
        print(f"Account Type: {currentUser.permType}")

        print("Press return to return to the main menu.")
        input()


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
    mainView = None

    def __init__(self, title, mainView, subTitle = "", permLevel = ""):
        super().__init__(title, subTitle=subTitle, permLevel=permLevel)
        self.mainView = mainView

    def render(self):
        super().render()

        print("Enter the books ISBN:")
        enteredISBN = input()
        enteredISBN = int(enteredISBN) if enteredISBN.isdigit() else None
        while enteredISBN == None and len(str(enteredISBN)) < 13:
            print("ISBN can not be empty and has to be a number containing 13 digits!")
            print("Enter the books ISBN:")
            enteredISBN = input()
            enteredISBN = int(enteredISBN) if enteredISBN.isdigit() else None
            
        print("Enter the books title:")
        enteredTitle = input()
        while enteredTitle == "":
            print("The title can not be empty!")
            print("Enter the books title:")
            enteredTitle = input()

        print("Enter the name of the books author:")
        enteredAuthor = input()
        while enteredAuthor == "":
            print("The author can not be empty!")
            print("Enter the name of the books author:")
            enteredAuthor = input()

        print("Enter the country the book was published in:")
        enteredCountry = input()
        while enteredCountry == "":
            print("The country can not be empty!")
            print("Enter the country the book was published in:")
            enteredCountry = input()

        print("Enter the language the book was written in:")
        enteredLanguage = input()
        while enteredLanguage == "":
            print("The language can not be empty!")
            print("Enter the language the book was written in:")
            enteredLanguage = input()

        print("Enter the amount of pages the book has:")
        enteredPages = input()
        enteredPages = int(enteredPages) if enteredPages.isdigit() else None
        while enteredPages == None:
            print("The amount of pages can not be empty and has to be a number!")
            print("Enter the amount of pages the book has:")
            enteredPages = input()
            enteredPages = int(enteredPages) if enteredPages.isdigit() else None

        print("Enter the year the book was published:")
        enteredYear = input()
        enteredYear = int(enteredYear) if enteredYear.isdigit() else None
        while enteredYear == None:
            print("The year can not be empty and has to be a number!")
            print("Enter the year the book was published:")
            enteredYear = input()
            enteredYear = int(enteredYear) if enteredYear.isdigit() else None

        print("Enter a link to the books description:")
        enteredLink = input()
        while enteredLink == "":
            print("The link can not be empty!")
            print("Enter a link to the books description:")
            enteredLink = input()

        print("Enter a link to the books image:")
        enteredImgLink = input()
        while enteredImgLink == "":
            print("The image link can not be empty!")
            print("Enter a link to the books image:")
            enteredImgLink = input()

        catalog.addBook(enteredISBN, enteredTitle, enteredAuthor, enteredCountry, enteredLanguage, enteredPages, enteredYear, enteredLink, enteredImgLink)

        print("Book has been added. Press return to return to the main menu.")
        input()

        self.mainView.render()


class AccountDeletion(View):
    def render(self):
        super().render()

        print("Enter the username of the account you want to delete:")
        enteredUsername = input()

        while enteredUsername == "":
            print("The username can not be empty.")
            print("Enter the username of the account you want to delete:")
            enteredUsername = input()

        user = dataStore.getPersonByUsername(enteredUsername)

        if user != None:
            print(f"Are you sure you want to delete the user {user.username}, {user.givenName} {user.surname} (Y/N)?")
            shouldDelete = input()

            if shouldDelete == "Y" or shouldDelete == "Yes" or shouldDelete == "y" or shouldDelete == "yes":
                dataStore.deletePerson(user)
                print("The user has been deleted. Press return to return to the main menu.")
                input()
            else:
                print("Aborted. Press return to return to the main menu.")
                input()
        else:
            print("No user by this username found!")
            self.render()


class ImportBooks(View):
    def render(self):
        super().render()

        print("Enter the path to the JSON file containing the books:")
        enteredPath = input()
        while enteredPath == "":
            print("The file path can not be empty!")
            print("Enter the path to the JSON file containing the books:")
            enteredPath = input()

        with open(enteredPath) as json_file:
            data = json.load(json_file)
            
            for book in data:
                if 'isbn' not in book:
                    print("!! No ISBN, generating a random one...")
                    book['isbn'] = random.randint(1111111111111, 9999999999999)

                    while self.bookInSystem(book['isbn'], book['title']):
                        book['isbn'] = random.randint(1111111111111, 99999999)

                if not self.bookInSystem(book['isbn'], book['title']):
                    catalog.addBook(book['isbn'], book['title'], book['author'], book['country'], book['language'], book['pages'], book['year'], book['link'], book['imageLink'])
                    print(f"Book {book['title']} - {book['isbn']} saved to system. ")
                else:
                    print(f"Book {book['title']} - {book['isbn']} already in system, skipping... ")

            print("All books have been added. Press return to return to the main menu.")
            input()

    def bookInSystem(self, isbn, title):
        for book in catalog.books:
            if book.isbn == isbn or book.title == title:
                return True
        
        return False


class ImportUsers(View):
    def render(self):
        super().render()

        print("Enter the path to the file (JSON or CSV) containing the users:")
        enteredPath = input()
        while enteredPath == "":
            print("The file path can not be empty!")
            print("Enter the path to the file (JSON or CSV) containing the users:")
            enteredPath = input()

        name, extension = os.path.splitext(enteredPath)

        if extension == ".json":
            with open(enteredPath) as json_file:
                data = json.load(json_file)
                self.importUserData(data)
        elif extension == ".csv":
            with open(enteredPath) as csvfile:
                data = csv.DictReader(csvfile)
                self.importUserData(data)

    def importUserData(self, data):
        for user in data:

            username = ""
            if 'Username' in user:
                username = user['Username']
            elif 'username' in user:
                username = user['username']

            if dataStore.usernameInUse(username):
                print(f"Skipping {username}, user already in system!")
            else:
                password = ""
                if 'Password' in user:
                    password = user['Password']
                elif 'password' in user:
                    password = user['password']
                else:
                    print("No password set in backup file, using 'password' as password.")
                    password = "password"

                givenName = ""
                if 'GivenName' in user:
                    givenName = user['GivenName']
                elif 'givenName' in user:
                    givenName = user['givenName']

                surname = ""
                if 'Surname' in user:
                    surname = user['Surname']
                elif 'surname' in user:
                    surname = user['surname']

                streetAddress = ""
                if 'StreetAddress' in user:
                    streetAddress = user['StreetAddress']
                elif 'streetAddress' in user:
                    streetAddress = user['streetAddress']

                city = ""
                if 'City' in user:
                    city = user['City']
                elif 'city' in user:
                    city = user['city']

                zipCode = ""
                if 'ZipCode' in user:
                    zipCode = user['ZipCode']
                elif 'zipCode' in user:
                    zipCode = user['zipCode']

                emailAddress = ""
                if 'EmailAddress' in user:
                    emailAddress = user['EmailAddress']
                elif 'emailAddress' in user:
                    emailAddress = user['emailAddress']

                telephoneNumber = ""
                if 'TelephoneNumber' in user:
                    telephoneNumber = user['TelephoneNumber']
                elif 'telephoneNumber' in user:
                    telephoneNumber = user['telephoneNumber']

                nameSet = ""
                if 'NameSet' in user:
                    nameSet = user['NameSet']
                elif 'nameSet' in user:
                    nameSet = user['nameSet']

                permType = ""
                if 'PermType' in user:
                    permType = user['PermType']
                elif 'permType' in user:
                    permType = user['permType']
                else:
                    permType = "Subscriber"

                person = Person(username, password, givenName, surname, streetAddress, city, zipCode, emailAddress, telephoneNumber, nameSet, permType)
                
                dataStore.addPerson(person)

        print("All users have been added. Press return to return to the main menu.")
        input()


class CreateBackup(View):
    def render(self):
        super().render()

        print("Exporting books to books.json...")
        rawBooks = dataStore.books
        books = []

        for book in rawBooks:
            books.append(book.__dict__)

        jsonString = json.dumps(books)
        jsonFile = open("books.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()

        print("Exporting persons to persons.json...")
        rawPersons = dataStore.persons
        persons = []

        for person in rawPersons:
            persons.append(person.__dict__)

        jsonString = json.dumps(persons)
        jsonFile = open("persons.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()


class LoanList(View):
    def render(self):
        super().render()
        
        loans = loanAdministration.getLoansByUser(currentUser)
        
        for loan in loans:
            book = loan.book

            print(book.isbn, book.title, book.author)

        print("Press return to return to the main menu.")
        input()


'''
    Initialize Main UI
'''
mainScreen = MainScreen("Main Menu")