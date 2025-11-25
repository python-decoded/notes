from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import BaseModel, BookModel


engine = create_async_engine("sqlite+aiosqlite:///test.db")
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db(session: AsyncSession):

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    session.add(BookModel(isbn="9667047393", name="Harry Potter"))
    session.add(BookModel(isbn="9786175851296", name="Bartimaeus"))
    session.add(BookModel(isbn="9786175851647", name="Lockwood & Co"))
    await session.commit()


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
