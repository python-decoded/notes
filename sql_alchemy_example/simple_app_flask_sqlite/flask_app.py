# install:     pip install Flask
# run command: flask --app flask_app run
# host, port:  http://127.0.0.1:5000

import sqlite3
from flask import Flask, request


URL = "my_database.db"
app = Flask(__name__)


@app.route('/book')
def show_books():
    count = request.args.get('count') or 100
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Books LIMIT ?", (count,))
        rows = cursor.fetchall()
    return [dict(zip(["book_id", "book_name"], row)) for row in rows]


@app.route('/book/<int:book_id>', methods=['GET'])
def show_book(book_id):
    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Books WHERE book_id = ?", (book_id,))
        row = cursor.fetchone()
    return dict(zip(["book_id", "book_name"], row))


@app.post('/book')
def create_book():
    data = request.get_json()

    with sqlite3.connect(URL) as connection:
        cursor = connection.cursor()
        cursor.execute(""" SELECT count(*) from Books; """)
        next_id = cursor.fetchone()[0] + 1

        cursor.execute(""" INSERT INTO Books (book_id, book_name) VALUES (?, ?); """,
                       [next_id, data["book_name"]])

    return {"book_id": next_id, "book_name": data["book_name"]}
