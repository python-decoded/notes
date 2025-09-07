import time
from multiprocessing import Process

data = []


def func(name="Child"):
    print(f"'{name}' job 1")
    time.sleep(0.1)
    data.append(name)


if __name__ == '__main__':
    print("Main 1")
    t = Process(target=func)
    t.start()
    print("Main 2")
    t.join()
    print(data)
