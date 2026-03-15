from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    books: list["Book"] = Relationship(back_populates="user")


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="books")


from sqlmodel import Session, create_engine, select

engine = create_engine("sqlite:///")
SQLModel.metadata.create_all(engine)


user = User(
    name="John",
    books=[
        Book(title="first_book"),
        Book(title="second_book")
    ]
)

with Session(engine) as session:
    session.add(user)
    session.commit()
    session.refresh(user)

with Session(engine) as session:
    user = session.exec(select(User).where(User.name == "John")).first()

    print(user)
    print(user.books)
