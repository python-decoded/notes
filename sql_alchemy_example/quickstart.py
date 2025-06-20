from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, relationship)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user",
                                                      cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


from sqlalchemy import create_engine
engine = create_engine("sqlite://", echo=True)


# Створити усі таблиці
Base.metadata.create_all(engine)

spongebob = User(name="spongebob",
                 fullname="Spongebob Squarepants",
                 addresses=[Address(email_address="spongebob@sqlalchemy.org")])

sandy = User(name="sandy",
             fullname="Sandy Cheeks",
             addresses=[Address(email_address="sandy@sqlalchemy.org"),
                        Address(email_address="sandy@squirrelpower.org")])

patrick = User(name="patrick", fullname="Patrick Star")



from sqlalchemy.orm import Session


with Session(engine) as session:
    session.add_all([spongebob, sandy, patrick])
    session.commit()


from sqlalchemy import select

# Простий Селект
stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))

with Session(engine) as session:
    for user in session.scalars(stmt):
        print("\n\n", user, *user.addresses, "\n", sep="\n")


with Session(engine) as session:

    #  Селект із Джойном
    stmt = (
        select(Address)
        .join(Address.user)
        .where(User.name == "sandy")
        .where(Address.email_address == "sandy@sqlalchemy.org")
    )
    sandy_address = session.scalars(stmt).one()
    print(sandy_address.email_address)

    # Оновлення Звичайного Поля
    sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"
    session.commit()


with Session(engine) as session:

    stmt = select(User).where(User.name == "patrick")
    patrick = session.scalars(stmt).one()

    # Оновлення Поля, що асоційованим Об'єктом
    patrick.addresses.append(
        Address(email_address="patrickstar@sqlalchemy.org")
    )
    session.commit()


# Видалення Даних
with Session(engine) as session:
    session.delete(patrick)
    session.commit()
