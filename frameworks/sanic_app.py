# install:          pip install sanic[ext]
# run server:       sanic sanic_app
# host, port:       http://127.0.0.1:8000

from dataclasses import dataclass, asdict

from sanic import Sanic, json
from sanic_ext import validate

app = Sanic(__name__)

# in memory db
BOOKS_DB = [{"book_id": 0, "book_name": "Hi there"},
            {"book_id": 1, "book_name": "How are you?"}]


@app.route("/book")
async def show_books(request):
    count = request.args.get("count")
    count = int(count) if count else None
    return json({"books": BOOKS_DB[:count]})


@app.route('/book/<book_id:int>', methods=["GET"])
async def show_book(request, book_id):
    return json({book["book_id"]: book for book in BOOKS_DB}[book_id])


@dataclass
class Book:
    book_name: str
    book_id: int | None = None


@app.post('/book')
@validate(json=Book)
async def create_book(request, body: Book):
    data = asdict(body)
    data["book_id"] = int(len(BOOKS_DB))
    BOOKS_DB.append(data)
    return json(data)
