order = {
    "id": "ord_9f3a21",
    "status": "paid",
    "currency": "USD",
    "user": {
        "id": 42,
        "email": "user@example.com",
        "name": "John Doe",
        "addresses": {
            "shipping": {
                "city": "New York",
                "street": "Madison Ave",
                "zip": "10022"
            },
            "billing": {
                "city": "New York",
                "street": "5th Avenue",
                "zip": "10001"
            }
        }
    }
}


match order:
    case {
        "status": "paid",
        "user": {
            "name": str(user_name),
            "email": str(user_email),
            "addresses": {
                "shipping": {
                    "city": shipping_city,
                    "street": shipping_street
                }
            }
        }
    }:
        print(f"Відправити сплачений товар на {shipping_city}, {shipping_street} для {user_name}")
    case _:
        print("Не вдалося знайти адресу для відправлення замовлення")
