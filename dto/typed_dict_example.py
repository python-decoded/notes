# file name:  typed_dict_example.py
# pip install mypy
# mypy typed_dict_example.py

from typing import TypedDict, NotRequired

Address = TypedDict('Address', {'city': str,
                                'country': str})
User = TypedDict('User', {'name': str,
                          'age': int,
                          'maried': bool,
                          'car': NotRequired[str | None],
                          "emails": list[str] | None,
                          "address": Address,
                          "credit_card": str})

user: User = {
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
    },

    "FOOOOO": 1234
}
