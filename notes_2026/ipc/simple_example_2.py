import multiprocessing as mp

global_data = []


def child_process(data: list):
    print("Child process started...")

    data.append(123)

    print("Child process ended.")


# parent process
if __name__ == "__main__":
    p = mp.Process(target=child_process,
                   args=(global_data,))
    p.start()
    p.join()

    print(f"{global_data=}")


