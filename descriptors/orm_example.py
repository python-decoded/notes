# we assume you have DB with 2 tables: Movie, Song


class Field:

    def __set_name__(self, owner, name):
        self.fetch = f'SELECT {name} FROM {owner.table} WHERE {owner.key}=?;'
        self.store = f'UPDATE {owner.table} SET {name}=? WHERE {owner.key}=?;'

    def __get__(self, obj, objtype=None):
        return conn.execute(self.fetch, [obj.key]).fetchone()[0]

    def __set__(self, obj, value):
        conn.execute(self.store, [value, obj.key])
        conn.commit()


class Movie(BaseModel):
    table = 'Movies'                    # Table name
    key = 'title'                       # Primary key
    director = Field()
    year = Field()

    def __init__(self, key):
        self.key = key


class Song(BaseModel):
    table = 'Music'
    key = 'title'
    artist = Field()
    year = Field()
    genre = Field()

    def __init__(self, key):
        self.key = key


# create connection
import sqlite3
conn = sqlite3.connect('entertainment.db')


# get value
Movie('Star Wars').director

jaws = Movie('Jaws')
print(f'Released in {jaws.year} by {jaws.director}')

print(Song('Country Roads').artist)

# update value
Movie('Star Wars').director = 'J.J. Abrams'
print(Movie('Star Wars').director)
