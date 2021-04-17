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

