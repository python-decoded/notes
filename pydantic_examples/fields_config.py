# pip install pydantic[email]

from enum import StrEnum
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, PositiveInt, SecretStr


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class Address(BaseModel):
    country: str
    city: str


class User(BaseModel):
    name: str = Field(pattern="^[A-Z][a-z]+$")
    age: PositiveInt

    uuid: UUID = Field(default_factory=uuid4)
    password: SecretStr = Field(min_length=8, alias="pass")
    married: bool = False
    car: Optional[str] = None
    user_role: UserRole = Field(default=UserRole.USER,
                                examples=["user", "admin"],
                                description="Role in system")
    birth_day: datetime
    emails: list[EmailStr] = Field(default_factory=list)
    address: Address


data = {
    "uuid": "7a64ba99-e226-407a-86d0-e050a14b5f47",
    "name": "John",
    "age": 35,
    "pass": "Password123",
    "married": True,
    "car": "Porsche",
    "user_role": "user",

    "birth_day": "1990-05-12",
    "emails": ["john@gmail.com",
               "superman@gmail.com"],
    "address": {
        "country": "Ukraine",
        "city": "Kyiv"
    }
}


user = User(**data)
user = User.model_validate(data)
print(user)
print(user.model_dump())
print(user.model_dump(by_alias=True))
print(user.model_dump_json(exclude=["uuid", "password", "address"]))
print(user.model_dump_json(exclude={"uuid": True, "birth_day": True, "address": ["country"]}))
