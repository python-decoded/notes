from datetime import datetime
from pydantic import (BaseModel, Field, SecretStr, model_serializer,
                      SerializerFunctionWrapHandler, SerializationInfo)


class Address(BaseModel):
    country: str
    city: str
    street: str
    house_number: int

    @model_serializer(when_used="json", mode="wrap")
    def serialize(self, serializer: SerializerFunctionWrapHandler):
        data = serializer(self)
        return " ".join(str(v) for v in data.values())


class User(BaseModel):
    name: str = Field()
    password: SecretStr = Field(exclude=True)
    birth_day: datetime
    address: Address

    @model_serializer
    def serialize(self, info: SerializationInfo):
        data = {"name": self.name, "birth_day": self.birth_day, "address": self.address,
                "password": self.password.get_secret_value()}

        show_password = info.context and info.context.get("show_password")
        if not show_password:
            data.pop("password")

        return data


user = User(
    name="John",
    password=SecretStr("Password123"),
    birth_day=datetime(1990, 5, 12),
    address=Address(country="Ukraine", city="Kyiv", street="Protasova", house_number=15)
)

print(*user.model_dump(context={"show_password": True}).items(), sep='\n', end='\n\n')
print(*user.model_dump_json(context={"show_password": True}).split(","), sep='\n', end='\n\n')
