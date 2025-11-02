from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import BaseModel


class BookModel(BaseModel):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(256))

    def __repr__(self):
        return f"Book №{self.id} [{self.isbn}] '{self.name}'"
