
class MyDescriptor:

    def __set_name__(self, owner, name):
        print(f"call __set_name__ {name}")
        self.attr_name = "_" + name

    def __get__(self, instance, owner):
        print(f"call __get__ {self.attr_name}")
        return getattr(instance, self.attr_name)

    def __set__(self, instance, value):
        print(f"call __set__ {self.attr_name}")
        setattr(instance, self.attr_name, value)

    def __delete__(self, instance):
        print(f"call __set__ {self.attr_name}")
        delattr(instance, self.attr_name)


class Some:
    some_attr = MyDescriptor()
    other_attr = MyDescriptor()


item = Some()
item.some_attr = 10
item.some_attr += 5
print(item.some_attr)

item.other_attr = "foo"
del item.other_attr

print(vars(item))
