from typing import Generic, TypeVar

T = TypeVar("T")  # Generic Type Variable


class Collection(Generic[T]):

    def __init__(self, data: list[T]):
        self.data = data

    def append(self, item: T):
        self.data.append(item)

    def pop(self) -> T:
        return self.data.pop()


collection = Collection([1, 2, 3])
collection.append("1")  # Expected type 'int' (matched generic type 'T'), got 'str' instead
collection.pop().lower()  # Unresolved attribute reference 'lower' for class 'int'


# python 3.12+

class Collection[T]:

    def __init__(self, data: list[T]):
        self.data = data

    def append(self, item: T):
        self.data.append(item)

    def pop(self) -> T:
        return self.data.pop()


collection = Collection([1, 2, 3])
collection.append("1")  # Expected type 'int' (matched generic type 'T'), got 'str' instead
collection.pop().lower()  # Unresolved attribute reference 'lower' for class 'int'
