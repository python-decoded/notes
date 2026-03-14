from sqlalchemy import create_engine, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    age: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    secret: Mapped[str] = mapped_column(String)


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///", connect_args=connect_args)
Base.metadata.create_all(engine)










john = User(name="John", age=15, secret="MyPassword123")
mathew = User(name="Mathew", age=35, secret="J0sjeY083")
anna = User(name="Anna", age=29, secret="FooBuzzBarr")

print("Users:", john, mathew, anna, sep="\n")


with Session(engine) as session:
    session.add(john)
    session.add_all([mathew, anna])
    session.commit()

    print("Users after commit:", john, mathew, anna, sep="\n")

    for user in [john, mathew, anna]:
        session.refresh(user)

    print("Users after refresh:", john, mathew, anna, sep="\n")


with Session(engine) as session:
    mathew = session.get(User, 2)
    print(mathew)

    query = select(User).where(User.age > 20).offset(0).limit(100)
    users = session.execute(query).scalars().all()
    print(*users, sep="\n")
