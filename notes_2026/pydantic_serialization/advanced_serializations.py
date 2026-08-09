from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, computed_field, PlainSerializer


def handler(v: float) -> str:
    return format(v, ",.2f") + "$"

DollarField = Annotated[float, PlainSerializer(handler)]


class Order(BaseModel):
    price: DollarField
    quantity: int
    date: datetime

    @computed_field(return_type=DollarField)
    def total(self) -> float:
        return self.price * self.quantity


order = Order(price=14.23, quantity=2,date="2025-10-15")

print(*order.model_dump().items(), sep='\n', end='\n\n')
print(order.model_dump_json().replace(',', '\n'))
