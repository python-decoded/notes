
books_db = [{"name": "Harry Potter", "isbn": "9667047393"},
            {"name": "Bartimaeus", "isbn": "9786175851296"},
            {"name": "Lockwood & Co", "isbn": "9786175851647"}]


from fastapi import APIRouter
from schemas.books import Book

router = APIRouter()


@router.get("/")
async def books(count: int = 10, offset: int = 0) -> list[Book]:
    return books_db[offset: offset + count]


@router.get("/{isbn}")
async def books(isbn: str) -> Book:
    return {b["isbn"]: b for b in books_db}[isbn]


@router.post("/")
async def books(book: Book) -> Book:
    book_record = book.model_dump()
    books_db.append(book_record)
    return book
