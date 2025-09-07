import time

param = "foo"
data = []


def func(name="Child"):
    print(f"'{name}' job 1")
    time.sleep(0.1)
    print(f"'{name}' job 2")


print("Main 1")
func()
print("Main 2")
print("Main 3")
