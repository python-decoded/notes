data = {
    "id": "123",
    "name": "John",
    "birth_day": 599004000,  # 25-12-1988  timestamp
    "address": {
        "country": "Ukraine",
        "city": "Kyiv"
    },

    "foo": 123,
    "buzz": 325,
    "bar": 32452
}


# pip install dataclasses-json

from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined, CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Address:
    country: str
    city: str
    extra: CatchAll


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class User:
    id: int
    name: str
    birth_day: datetime
    address: Address
    extra: CatchAll


user = User.from_dict(data)
print(user)
print(user.id)
print(user.birth_day)
print(user.extra)
print(user.to_dict())
print(user.to_json())
