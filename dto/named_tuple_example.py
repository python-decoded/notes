from collections import namedtuple

User = namedtuple("User", ["name", "age", "email"])
user = User("John", 25, "john@gmail.com")

name = user[0]
name = user.name

try:
    user.name = "Mathew"
except AttributeError:
    pass


data = ["John", 32, "foo@gmail.com"]
user = User(*data)

data = {"name": "John", "age": 25, "email": "foo@gmail.com"}
user = User(**data)


for i in user:
    print(i)


fields = user[0:2]
name, age, *_ = user


data = user._asdict()


Vector2 = namedtuple("Vector2", ["x", "y"])
vector = Vector2(1.4, 3.2)

x = vector.x
x, y = vector
print(x, y)
