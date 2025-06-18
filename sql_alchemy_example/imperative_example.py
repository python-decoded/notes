from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine


metadata = MetaData()


user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(30)),
    Column("email", String, nullable=True),
)


engine = create_engine("sqlite://")

metadata.create_all(engine)


insert_query = user_table.insert().values(username="John", email="John@gmail.com")
select_query = user_table.select().where(user_table.c.username == "John")


with engine.connect() as connection:

    connection.execute(insert_query)
    result = connection.execute(select_query)
    user = result.fetchone()

    print(user)









