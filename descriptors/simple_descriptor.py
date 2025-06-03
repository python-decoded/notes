
class MyDescriptor:

    def __get__(self, instance, owner):
        print("call __get__ ")
        return 10


class Some:
    ten = MyDescriptor()
    five = 5


item = Some()
print(item.five)
print(item.ten)
print(Some.five)
print(Some.ten)
