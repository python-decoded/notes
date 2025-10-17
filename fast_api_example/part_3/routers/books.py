
books_db = [{"name": "Harry Potter", "isbn": "9667047393"},
            {"name": "Bartimaeus", "isbn": "9786175851296"},
            {"name": "Lockwood & Co", "isbn": "9786175851647"}]


from fastapi import APIRouter
from fastapi import status, HTTPException
from schemas.books import Book


class AppBaseException(Exception): ...


class ItemNotFoundException(AppBaseException): ...


router = APIRouter()


@router.get("/")
async def books(count: int = 10, offset: int = 0) -> list[Book]:
    return books_db[offset: offset + count]


@router.get("/{isbn}")
async def books(isbn: str) -> Book:
    book = {b["isbn"]: b for b in books_db}.get(isbn)
    if not book:
        raise ItemNotFoundException(f"Book with isbn {isbn} not found")
    return book


@router.post("/", status_code=status.HTTP_201_CREATED)
async def books(book: Book) -> Book:
    book_ids = {b["isbn"] for b in books_db}

    if book.isbn in book_ids:
        raise HTTPException(status_code=400,
                            detail=f"Book with isbn {book.isbn} already exists.")

    book_record = book.model_dump()
    books_db.append(book_record)
    return book



