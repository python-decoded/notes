from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError

from schemas.books import Book
from models import BookModel
from deps import SessionDep
from exceptions import ItemNotFoundException


router = APIRouter()


@router.get("/")
async def books(session: SessionDep, count: int = 10, offset: int = 0) -> list[Book]:

    get_books_query = select(BookModel).order_by(desc(BookModel.id)).limit(count).offset(offset)
    books = (await session.scalars(get_books_query)).all()
    return [Book.model_validate(book, from_attributes=True) for book in books]


@router.get("/{isbn}")
async def books(session: SessionDep, isbn: str) -> Book:

    get_book_query = select(BookModel).where(BookModel.isbn == isbn)
    book = (await session.scalars(get_book_query)).one_or_none()

    if not book:
        raise ItemNotFoundException(f"Book with isbn {isbn} not found")
    return Book.model_validate(book, from_attributes=True)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def books(session: SessionDep, book: Book) -> Book:

    session.add(BookModel(isbn=book.isbn, name=book.name))

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=400,
                            detail=f"Book with isbn {book.isbn} already exists.")

    return book
