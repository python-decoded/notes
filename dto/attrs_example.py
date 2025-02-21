data = {
    "id": "123",
    "name": "John",
    "birth_day": 599004000,  # 25-12-1988  timestamp
    "address": {
        "country": "Ukraine",
        "city": "Kyiv"
    }
}

# pip install attrs

from datetime import datetime
from attrs import define, field, asdict


@define(frozen=True, order=True)
class Address:
    country: str
    city: str


@define(frozen=True, order=True)
class User:
    id: int = field(converter=int)
    name: str
    birth_day: datetime = field(converter=datetime.fromtimestamp)
    address: Address = field(converter=lambda i: Address(**i))


user = User(**data)
user_dict = asdict(user)
