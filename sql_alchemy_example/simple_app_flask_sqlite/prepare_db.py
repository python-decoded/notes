import sqlite3

URL = "my_database.db"


with sqlite3.connect("my_database.db") as connection:

    cursor = connection.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY,
        book_name TEXT NOT NULL
    );
    """)
