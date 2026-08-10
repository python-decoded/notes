from datetime import datetime
from pydantic import (BaseModel, computed_field, field_serializer,
                      SerializerFunctionWrapHandler)


class Order(BaseModel):
    price: float
    quantity: int
    date: datetime

    @computed_field
    def total(self) -> float:
        return self.price * self.quantity

    @field_serializer("price", "total",
                      when_used="json", mode="wrap")
    def handler(self, v: float, serializer: SerializerFunctionWrapHandler) -> str:
        # зробити щось до вбудованої серіалізації
        v = serializer(v)
        # зробити щось після вбудованої серіалізації
        return format(v, ",.2f") + "$"


order = Order(price=14.23, quantity=2,date="2025-10-15")

print(*order.model_dump().items(), sep='\n', end='\n\n')
print(*order.model_dump(mode="json").items(), sep='\n', end='\n\n')
print(order.model_dump_json().replace(',', '\n'))
