data = {
    "id": "123",
    "name": "John",
    "birth_day": 599004000,  # 25-12-1988
    "address": {
        "country": "Ukraine",
        "city": "Kyiv"
    }
}

from datetime import datetime
from dataclasses import dataclass


@dataclass
class Address:
    country: str
    city: str


@dataclass
class User:
    id: int
    name: str
    birth_day: datetime
    address: Address

    def __post_init__(self):
        self.id = int(self.id)
        self.birth_day = datetime.fromtimestamp(self.birth_day)
        self.address = Address(**self.address)


user = User(**data)
print(user)
print(user.id)
print(user.name)
print(user.birth_day.year)
print(user.address.city)
