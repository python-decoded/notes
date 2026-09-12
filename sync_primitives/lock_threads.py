import time
from threading import Thread, Lock

shared_obj = []
access_lock = Lock()


def t1_logic():
    access_lock.acquire()

    for i in range(5):
        time.sleep(0.01)
        shared_obj.append(f"t1 line {i}")

    access_lock.release()

def t2_logic():

    with access_lock:
        for i in range(5):
            time.sleep(0.01)
            shared_obj.append(f"t2 line {i}")


if __name__ == '__main__':
    t1  = Thread(target=t1_logic)
    t2  = Thread(target=t2_logic)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(*shared_obj, sep="\n")
