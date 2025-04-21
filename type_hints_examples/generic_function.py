from typing import TypeVar

T = TypeVar("T")  # Generic Type Variable


def get_first_item(collection: list[T]) -> T:
    return list(collection)[0]


res1 = get_first_item([1, 2, 3])
res2 = get_first_item(["1", "2", "3"])

res1.lower()  # Unresolved attribute reference 'lower' for class 'int'


# python 3.12+
def get_first_item[T](collection: list[T]) -> T:
    return list(collection)[0]


res1 = get_first_item([1, 2, 3])
res2 = get_first_item(["1", "2", "3"])

res1.lower()  # Unresolved attribute reference 'lower' for class 'int'
