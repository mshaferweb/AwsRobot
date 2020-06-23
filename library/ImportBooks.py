import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class ImportBooks:

    def __init__(self):
        self.load = True

    def setup_engine(self,url):
        # url = "postgresql://dbadmin:abcdefg123456789@hello4.cqa6jc4nxqdn.us-east-2.rds.amazonaws.com/books"
        self.engine = create_engine(url)
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def create_tables(self,url):
        self.setup_engine(url)
        sql_books = """CREATE TABLE books (
        id SERIAL PRIMARY KEY,
        isbn VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL,
        year INTEGER NOT NULL
    );"""
        sql_users = """CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        session_id INTEGER NOT NULL
    );"""
        sql_reviews = """CREATE TABLE reviews (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users,
        book_id INTEGER REFERENCES books,
        review VARCHAR NOT NULL,
        rating INTEGER NOT NULL
    );"""
        self.db.execute(sql_books)
        self.db.execute(sql_users)
        self.db.execute(sql_reviews)
        self.db.commit()
        return "Created books, users reviews table"

    def drop_tables(self,url):
        self.setup_engine(url)

        for table in ['users','reviews','books']:
            sql = 'DROP TABLE IF EXISTS '+table+' CASCADE;'
            self.db.execute(sql)
            self.db.commit()
        print("dropped tables!" )
        return("dropped tables!")
    def truncate_user_reviews(self,url):
        self.setup_engine(url)

        for table in ['reviews','users']:
            sql = 'TRUNCATE ' + table + ' CASCADE;'
            self.db.execute(sql)
            self.db.commit()
        print("done")

    def load_books(self,url):
        import concurrent.futures

        self.setup_engine(url)

        # isbn,title,author,year
        f = open("library/books.csv")
        reader = csv.reader(f)
        for isbn, title, author, year in reader:
            if isbn.__eq__('isbn'):
                continue

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                executor.map(thread_function, range(3))
            self.db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                        {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added Book: {isbn}  {title}")
        self.db.commit()
        print(f"Loaded books")
        return "Loaded books"


# book = ImportBooks()
# book.dropTables()
# book.createTables()
# book.loadBooks()