
item = 30

match item:
    case 10 | 20:
        print("Десять або Двадцять")
    case 30:
        print("Тридцять")
    case int(x) if x > 50:
        print(f"Щось інше, а саме {x}")
    case _:
        print(f"Щось інше")


# if else  аналог

if item in [10, 20]:
    print("Десять або Двадцять")
elif item == 30:
    print("Тридцять")
elif item > 50:
    print(f"Щось інше, а саме {item}")
else:
    print(f"Щось інше")


# парсинг ліста

items = [10, 20, 30]

match items:
    case (first, *other):
        print(f"Перший елемент {first}")
        print(f"Інші елементи {other}")
    case (first, second):
        print("Рівно 2 елементи")
    case ():
        print("Колекція пуста")
    case (first, 10, *other):
        print("Другий елемент == 10")



# парсинг словника

user = {"name": "John",
        "age": 35,
        "role": "admin",
        "books": [{"name": "Harry Potter"},
                  {"name": "Bartimaeus"}]}


match user:
    case {"name": user_name, **other}:
        print(f"Користувач {user_name}")
    case {"role": "admin"}:
        print(f"Користувач адміністратор")
    case {"age": user_age} if user_age >= 18:
        print(f"Користувач повнолітній")


# рекурсивна перевірка
match user:
    case {"books": [{"name": first_book_name}, *other]}:
        print(f"Користувач має книгу {first_book_name}")


# cпроба реалізувати перевірку звичайними засобами
if (books := user.get("books")):
    if (first_book_name := books[0].get("name")):
        print(f"Користувач має книгу {first_book_name}")


if user.get("books"):
    first_book = user["books"][0]
    if "name" in first_book:
        first_book_name = first_book["name"]
        print(f"Користувач має книгу {first_book_name}")


if (isinstance(user, dict)
        and (books := user.get("books"))
        and isinstance(books, list)):
   if isinstance(books[0], dict) and (book_name := books[0].get("name")):
            print(f"First book name is: {book_name}")


if  (isinstance(user, dict)
        and user.get("books")
        and isinstance(user["books"], list)):
    first_book = user["books"][0]
    if isinstance(first_book, dict) and "name" in first_book:
        book_name = first_book["name"]
        print(f"First book name is: {book_name}")



# перевірка типу даних
item = 10.5

match item:

    case int(_):
        print(f"item це int")

    case int(_) | float(_):
        print(f"item це int або float")

    case _:
        print(f"Будь-який item")




# парсинг за атрибутами

class User:

    __match_args__ = ("name", "age", "role")

    def __init__(self, user_name, user_role, user_age):
        self.name = user_name
        self.role = user_role
        self.age = user_age


user = User("John", "admin", 34)


match user:

    case User(name=name_of_user, age=age_of_user):
        print(f"Користувач {name_of_user}, вік {age_of_user}")

    case User(role="admin"):
        print(f"Користувач є адміністратором")

    case User(age=int(age_of_user)) if age_of_user >= 18:
        print(f"Користувач є повнолітнім")

    case User(str(_), int(user_age), "admin"):
        print(f"Користувач є адміністратором")

    case User():
        print("Це користувач")

    case User() as current_user:
        print(f"Це користувач {current_user.name}")

    case User(str() as name):
        print(f"Це користувач {name}")
