
class MyDescriptor:

    def __init__(self, file_name):
        self.file_name = file_name

    def __get__(self, instance, owner):
        with open(f"data/{self.file_name}.txt") as f:
            return f.read()


class Some:
    file_1 = MyDescriptor("file_1")
    file_2 = MyDescriptor("file_2")


item = Some()
print(item.file_1)
print(item.file_2)


# retrieval of param from instance

class OtherDescriptor:

    def __get__(self, instance, owner):
        with open(f"data/{instance.file_name}.txt") as f:
            return f.read()


class Other:
    file_content = OtherDescriptor()

    def __init__(self, file_name):
        self.file_name = file_name


other_1 = Other("file_1")
other_2 = Other("file_2")
print(other_1.file_content)
print(other_2.file_content)
