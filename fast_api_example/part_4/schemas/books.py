from pydantic import BaseModel


class Base(BaseModel):
    ...


class Book(Base):
    isbn: str
    name: str
