
class MyDescriptor:

    def validate(self, value):
        pass

    def __set_name__(self, owner, name):
        self.attr_name = "_" + name

    def __get__(self, instance, owner):
        print(f"call __get__ {self.attr_name}")
        return getattr(instance, self.attr_name)

    def __set__(self, instance, value):
        print(f"call __set__ {self.attr_name}")
        self.validate(value)
        setattr(instance, self.attr_name, value)


class PositiveInt(MyDescriptor):
    def validate(self, value):
        assert isinstance(value, int) and value >= 0


class OneOf(MyDescriptor):
    def __init__(self, values):
        self.values = values

    def validate(self, value):
        assert value in self.values


class Some:
    some_attr = PositiveInt()
    other_attr = OneOf(["foo", "buzz", "bar"])


item = Some()
item.some_attr = 10
item.other_attr = "foo"
