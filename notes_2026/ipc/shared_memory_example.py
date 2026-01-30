from multiprocessing import shared_memory, Process


def child_process(shared_memory):
    msg = b"Hello from child process"

    buffer = shared_memory.buf
    buffer[:len(msg)] = msg
    buffer[len(msg)] = 0  # кінець повідомлення
    shared_memory.close()


# parent process
if __name__ == "__main__":
    shared_memory = shared_memory.SharedMemory(create=True,
                                               size=128)

    p = Process(target=child_process,
                args=(shared_memory,))
    p.start()
    p.join()

    msg_end = shared_memory.buf.tobytes().find(b"\x00")
    msg = shared_memory.buf[:msg_end].tobytes().decode("utf-8")
    print(f"Message: '{msg}'")
    shared_memory.close()
