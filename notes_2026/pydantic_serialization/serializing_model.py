from datetime import datetime
from pydantic import (BaseModel, Field, SecretStr, model_serializer,
                      SerializerFunctionWrapHandler)


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


user = User(
    name="John",
    password=SecretStr("Password123"),
    birth_day=datetime(1990, 5, 12),
    address=Address(country="Ukraine", city="Kyiv", street="Protasova", house_number=15)
)

print(*user.model_dump().items(), sep='\n', end='\n\n')
print(*user.model_dump_json().split(","), sep='\n', end='\n\n')
