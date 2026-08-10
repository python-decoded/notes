from pydantic import BaseModel, model_serializer


class Product(BaseModel):
    sku: str
    name: str
    price: float


class OrderItem(BaseModel):
    product: Product
    quantity: int


class Customer(BaseModel):
    customer_id: int
    email: str


class Order(BaseModel):
    order_id: str
    customer: Customer
    items: list[OrderItem]

    @model_serializer
    def to_flat_shipping_manifest(self) -> list[dict]:
        flat_rows = []

        for item in self.items:
            # Створюємо один плаский рядок для кожної позиції в замовленні
            row = {
                "order_id": self.order_id,
                "customer_email": self.customer.email,
                "product_sku": item.product.sku,
                "product_name": item.product.name,
                "qty": item.quantity,
                "total_item_price": round(item.product.price * item.quantity, 2)
            }
            flat_rows.append(row)

        return flat_rows


order = Order(
    order_id="ORD-2026-99",
    customer=Customer(customer_id=42, email="buyer@example.com"),
    items=[
        OrderItem(product=Product(sku="LAP-12", name="Laptop", price=1200.00),
                  quantity=1),
        OrderItem(product=Product(sku="MOU-05", name="Wireless Mouse", price=45.50),
                  quantity=2),
    ]
)

# Викликаємо стандартний model_dump()
flat_data = order.model_dump()

import json

print(json.dumps(flat_data, indent=2, ensure_ascii=False))
