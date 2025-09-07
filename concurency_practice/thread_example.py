import time
from threading import Thread

param = "foo"
data = []


def func(name="Child"):
    print(f"'{name}' job 1")
    time.sleep(0.1)
    data.append(name)


print("Main 1")
t1 = Thread(target=func, daemon=True, args=("1st Child",))
t2 = Thread(target=func, daemon=True, args=("2nd Child",))
t1.start()
t2.start()
print("Main 2")
t1.join()
t2.join()
print(data)
