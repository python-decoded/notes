from enum import StrEnum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, SecretStr, ConfigDict, computed_field


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class Address(BaseModel):
    country: str
    city: str


class User(BaseModel):

    model_config = ConfigDict(serialize_by_alias=True,
                              alias_generator=lambda alias: alias.replace("_", " ").title().replace(" ", ""),
                              validate_by_name=True,
                              ser_json_temporal="iso8601",
                              ser_json_timedelta="iso8601",
                              ser_json_bytes="utf8",
                              ser_json_inf_nan="null")

    name: str = Field()
    password: SecretStr = Field(exclude=True)
    married: bool = False
    car: Optional[str] = None
    birth_day: datetime
    user_role: UserRole = Field(default=UserRole.USER)
    address: Address

    @computed_field
    def foo(self) -> int:
        return 42

user = User(
    name="John",
    password=SecretStr("Password123"),
    car=None,
    user_role=UserRole.USER,
    birth_day=datetime(1990, 5, 12),
    address=Address(country="Ukraine", city="Kyiv")
)


print(user.model_dump())
print(user.model_dump(mode="json"))
print(user.model_dump_json())

print(user.model_dump(by_alias=True))
print(user.model_dump_json(exclude={"password", "address", "birth_day"}))
print(user.model_dump_json(include={"name", "user_role"}))

print(user.model_dump_json(exclude={"uuid", "password", "address"}))
print(user.model_dump_json(exclude={"uuid": True, "birth_day": True, "address": {"country"}}))
print(user.model_dump_json(include={"name": True, "user_role": True, "address": {"country"}}))

print(user.model_dump(exclude_unset=True))
print(user.model_dump(exclude_defaults=True))
print(user.model_dump(exclude_none=True))
print(user.model_dump(exclude_computed_fields=True))
