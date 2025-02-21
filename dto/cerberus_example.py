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


# pip install cerberus

from cerberus import Validator

v = Validator({
    'name': {'type': 'string'},
    'age': {'type': 'integer'},
    'maried': {'type': 'boolean'},
    'car': {'type': 'string', 'required': False, 'nullable': True},
    'emails': {'type': 'list'},
    'address': {
        'type': 'dict',
        'schema': {
            'country': {'type': 'string'},
            'city': {'type': 'string'}
        }
    },

    "credit_card": {'type': 'string', "required": True}
})


if not v.validate(user):
    print("User does not match schema")
    print(v.errors)
