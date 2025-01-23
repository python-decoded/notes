import random
import math


def prepare_table():

    errors = [k for k in dir(__builtins__)
              if isinstance(getattr(__builtins__, k), type)
              and issubclass(getattr(__builtins__, k), Exception)
              and getattr(__builtins__, k) is not Exception
              and not issubclass(getattr(__builtins__, k), (Warning, ExceptionGroup))]

    print(f"Errors Found: {len(errors)}")
    random.shuffle(errors)

    cols = 3
    rows = math.ceil(len(errors) / cols)

    for i in range(rows):
        print(*[r.center(25, "_") for r in errors[cols * i: cols * (i + 1)]])


if __name__ == "__main__":
    prepare_table()
