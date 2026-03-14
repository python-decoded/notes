from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret: str


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///", connect_args=connect_args)
SQLModel.metadata.create_all(engine)

john = User(name="John", age=18, secret="MyPassword123")
print("User:", john)

mathew = User(name="Mathew", age=35, secret="J0sjeY083")
anna = User(name="Anna", age=29, secret="FooBuzzBarr")

with Session(engine) as session:
    session.add(john)
    session.add_all([mathew, anna])

    session.commit()
    session.refresh(john)
    print("User after refresh:", john)

with Session(engine) as session:
    mathew = session.get(User, 2)
    print(mathew)

    query = select(User).where(User.age > 20).offset(0).limit(100)
    users = session.exec(query).all()
    print(*users, sep="\n")
