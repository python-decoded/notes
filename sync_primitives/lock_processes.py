import time
from multiprocessing import Process, Lock

access_lock = Lock()


def t1_logic(lock):
    res = lock.acquire(timeout=10)

    if res is False:
        return

    for i in range(5):
        time.sleep(0.01)
        print(f"t1 line {i}")

    lock.release()

def t2_logic(lock):

    with lock:
        for i in range(5):
            time.sleep(0.01)
            print(f"t2 line {i}")


if __name__ == '__main__':
    t2  = Process(target=t1_logic, args=(access_lock, ))
    t1  = Process(target=t2_logic, args=(access_lock, ))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
