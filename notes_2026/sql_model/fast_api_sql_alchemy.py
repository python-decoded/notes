from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


Base = declarative_base()


class DBUser(Base):
    __tablename__ = "user"

    id: int | None = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    age: int | None = Column(Integer, nullable=True)
    secret: str = Column(String)


class User(BaseModel):

    id: int | None = Field(default=None)
    name: str
    age: int | None = Field(default=None)
    secret: str


connect_args = {"check_same_thread": False}
engine = create_engine("sqlite:///database.db", connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# ============================================================================

@app.get("/users", response_model=list[User])
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    db_users = session.query(DBUser).offset(offset).limit(limit).all()
    return db_users


@app.post("/users", response_model=User)
def create_user(hero: User, session: SessionDep) -> DBUser:
    db_user = DBUser(**hero.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: SessionDep) -> DBUser:
    db_user = session.get(DBUser, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
