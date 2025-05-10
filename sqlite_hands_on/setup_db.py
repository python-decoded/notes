import sqlite3


with sqlite3.connect("my_database.db") as connection:

    cursor = connection.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.executescript("""
    INSERT INTO Users (username, email) VALUES ('newuser', 'newuser@example.com');
    INSERT INTO Users (username, email) VALUES ('other', 'other@example.com');
    INSERT INTO Users (username, email) VALUES ('some', 'some@example.com');
    """)

    connection.commit()  # If there is no open transaction, this method is a no-op.

    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()
    print(*rows, sep="\n")

    row = cursor.execute("SELECT * FROM Users WHERE username = ?", ("other", )).fetchone()
    print("\n", row)
