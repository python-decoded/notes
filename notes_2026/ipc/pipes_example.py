import time
import multiprocessing


def child_process(read_conn):
    print("Child Process listening Pipe...")
    msg = read_conn.recv()
    print(f"Received {msg=}")


# parent process
if __name__ == "__main__":
    write_conn, read_conn = multiprocessing.Pipe()

    p = multiprocessing.Process(target=child_process,
                                args=(read_conn,))
    p.start()

    time.sleep(5)
    write_conn.send("Hello from Parent Process!")
    write_conn.close()


