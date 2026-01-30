import os
import time
import multiprocessing
import datetime
import signal


def child_process():
    print("Child process started...")

    while True:
        print(datetime.datetime.now())
        time.sleep(1)


# parent process
if __name__ == "__main__":
    p = multiprocessing.Process(target=child_process)
    p.start()

    print(f"[parent] Child PID={p.pid}")

    time.sleep(3)
    print("[parent] OS pause (SIGSTOP)")
    os.kill(p.pid, signal.SIGSTOP)

    time.sleep(2)
    print("[parent] OS resume (SIGCONT)")
    os.kill(p.pid, signal.SIGCONT)

    time.sleep(3)
    print("[parent] Soft shutdown (SIGTERM)")
    os.kill(p.pid, signal.SIGTERM)

    p.join()
    print("[parent] Child exited")
