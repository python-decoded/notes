from datetime import datetime
from pydantic import BaseModel, computed_field


class Order(BaseModel):

    price: float
    quantity: int
    date: datetime

    @computed_field
    def total(self) -> float:
        return self.price * self.quantity


order = Order(
    price=14.23,
    quantity=2,
    date=datetime(2025, 10, 15)
)


print(order.model_dump_json())
