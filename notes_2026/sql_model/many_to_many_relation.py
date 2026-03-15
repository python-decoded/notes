from sqlmodel import SQLModel, Field, Relationship

class UserBookLink(SQLModel, table=True):
    user_id: int | None = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    book_id: int | None = Field(
        default=None, foreign_key="book.id", primary_key=True
    )


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    books: list["Book"] = Relationship(back_populates="users",
                                       link_model=UserBookLink)


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

    users: list[User] = Relationship(back_populates="books",
                                     link_model=UserBookLink)



from sqlmodel import Session, create_engine, select

engine = create_engine("sqlite:///")
SQLModel.metadata.create_all(engine)


books = [Book(title="first_book"),
         Book(title="second_book")]
user_1 = User(name="John", books=books)
user_2 = User(name="Mathew", books=books)

with Session(engine) as session:
    session.add_all([user_1, user_2])
    session.commit()


with Session(engine) as session:
    book = session.exec(select(Book).where(Book.title == "first_book")).first()

    print(book)
    print(book.users)
    print(book.users[0])
    print(book.users[0].books)
