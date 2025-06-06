import time
from functools import cached_property


class MyClass:

    @cached_property
    def calculated_value(self):
        for _ in range(10):
            time.sleep(0.5)
            print(".", end="")
        print(".")

        return "IMPORTANT VALUE"


item = MyClass()
print(item.calculated_value)
vars(item)
print(item.calculated_value)
print(item.calculated_value)
print(item.calculated_value)
