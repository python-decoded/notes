from typing import Optional
from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[Optional[str]]


engine = create_engine("sqlite://")

Base.metadata.create_all(engine)


insert_user = User(username="John", email="John@gmail.com")
select_query = select(User).where(User.username == "John")



with Session(engine) as session:

    session.add(insert_user)
    row = session.scalars(select_query).one()

    print(row.id, row.username, row.email)


