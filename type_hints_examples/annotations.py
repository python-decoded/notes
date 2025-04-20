
a: int
b: str


class Foo:
    c: list
    d: dict


def func(e: set, f: bool):
    ...


print("module", __annotations__)

print("class", Foo.__annotations__)

print("func", func.__annotations__)
