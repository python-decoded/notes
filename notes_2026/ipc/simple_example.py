import multiprocessing as mp

global_data = []


def child_process():
    print("Child process started...")

    global_data.append(123)

    print("Child process ended.")


# parent process
if __name__ == "__main__":
    p = mp.Process(target=child_process)
    p.start()
    p.join()

    print(f"{global_data=}")


