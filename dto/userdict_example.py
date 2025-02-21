user = {
    "name": "John",
    "age": 25,
    "maried": False,
    "car": None,
    "emails": [
        "john@gmail.com",
        "superman@gmail.com"
    ],
    "address": {
        "country": "Ukraine",
        "city": "Kyiv"
    }
}


from collections import UserDict


class Address(UserDict):
    required = ["country", "city"]

    def __init__(self, data=None, /, **kwargs):
        assert set(self.required) <= data.keys(), "Missing required fields"
        super().__init__(data, **kwargs)

class User(UserDict):
    required = ["name", "age", "maried", "car", "emails", "address"]

    def __init__(self, data=None, /, **kwargs):
        assert set(self.required) <= data.keys(), "Missing required fields"
        super().__init__(data, **kwargs)
        self.data["address"] = Address(self.data["address"])


user = User(user)
name = user["name"]     # John
age = user.get("age")  # 25
city = user["address"]["city"]  # Kyiv
email = user["emails"][0]  # john@gmail.com
