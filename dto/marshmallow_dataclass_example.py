data = {
    "id": "123",
    "name": "John",
    "birth_day": 599004000,  # 25-12-1988  timestamp
    "address": {
        "country": "Ukraine",
        "city": "Kyiv"
    }
}


# pip install marshmallow-dataclass

from dataclasses import dataclass
from typing import Annotated

import marshmallow
import marshmallow_dataclass


@dataclass
class Address:
    country: str
    city: str


@dataclass
class User:
    id: int
    name: str
    birth_day: Annotated[int, marshmallow.fields.DateTime("timestamp")]
    address: Address


UserSchema = marshmallow_dataclass.class_schema(User)   # create marshmallow schema
user = UserSchema().load(data)
print(user)
data = UserSchema().dump(user)
print(data)
