
data = {"name": "John",
        "birth_day": 599004000}  # 25-12-1988


from datetime import datetime


class User:

    def __init__(self, name: str, birth_day: int):
        self.__name = name
        self.__birth_day = datetime.fromtimestamp(birth_day)

    @property
    def name(self):
        return self.__name

    @property
    def birth_day(self):
        return self.__birth_day

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["birth_day"])

    def as_dict(self):
        return {
            "name": self.name,
            "birth_day": self.birth_day.timestamp()
        }

    def __str__(self):
        return f"User({self.__name}, {self.__birth_day.isoformat()})"

    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (other.__name, other.__birth_day) == (self.__name, self.__birth_day)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, type(self)):
            return not self.__eq__(other)
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return (self.__name, self.__birth_day) < (other.__name, other.__birth_day)
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return (self.__name, self.__birth_day) > (other.__name, other.__birth_day)
        else:
            return NotImplemented

    def __lte__(self, other):
        if isinstance(other, type(self)):
            return (self.__name, self.__birth_day) <= (other.__name, other.__birth_day)
        else:
            return NotImplemented

    def __gte__(self, other):
        if isinstance(other, type(self)):
            return (self.__name, self.__birth_day) >= (other.__name, other.__birth_day)
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.__name, self.__birth_day))


user = User(**data)
print(user)
print(user.__name)
print(user.__birth_day.year)
