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