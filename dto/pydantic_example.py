# pip install pydantic

from datetime import datetime
from pydantic import BaseModel


class Address(BaseModel):
    city: str
    country: str


class User(BaseModel):
    id: int
    name: str
    birth_day: datetime
    address: Address


data = {
    "id": "123",
    "name": "John",
    "birth_day": 599004000,  # 25-12-1988  timestamp
    "address": {
        "country": "Ukraine",
        "city": "Kyiv"
    }
}

user = User(**data)
print(user)
print(user.id)
print(user.birth_day.year)
print(user.address.city)

data = user.model_dump()
print(data)
json_data = user.model_dump_json()
print(json_data)
