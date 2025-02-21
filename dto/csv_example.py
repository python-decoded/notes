
csv_data = """name,age,email
John,34,john@gmail.com
Mathew,25,foo@gmail.com
Linda,42,foo@gmail.com"""

headers, *rows = [l.split(",") for l in csv_data.splitlines()]


from collections import namedtuple

User = namedtuple("User", headers)
user = User(*rows[1])

print(user.name)   # Mathew
print(user.age)    # 25
print(user.email)  # foo@gmail.com
