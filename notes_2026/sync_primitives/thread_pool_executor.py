import asyncio
import time, random
# from concurrent.futures import ThreadPoolExecutor as PoolExecutor, as_completed
from concurrent.futures import ProcessPoolExecutor as PoolExecutor, as_completed


def process_message(text, number):
    print(f"Обробка повідомлення {number}...")
    time.sleep(random.random() * 4)
    return f"Повідомлення {number}: {len(text)} літер."

def process_result(future):
    print(f"ЗАВЕРШЕНО: {future.result()}")


if __name__ == '__main__':

    messages = ["Foo", "Hello", "How Are You",
                "Hi", "Buzz", "Good job", "Nice to see you",
                "I am fine", "Good to hear from you", "Good bye"]
    numbers = list(range(1, len(messages) + 1))

    print("\n\nMAP\n")
    with PoolExecutor(max_workers=4) as executor:
        results = executor.map(process_message, messages, numbers)
        print(*results, sep="\n")

    print("\n\nAS COMPLETED\n")
    futures = []
    with PoolExecutor(max_workers=4) as executor:
        for args in zip(messages, numbers):
            future = executor.submit(process_message, *args)
            futures.append(future)

        for future in as_completed(futures):
            print(future.result())

    print("\n\nWITH CALLBACK\n")

    with PoolExecutor(max_workers=4) as executor:
        for args in zip(messages, numbers):
            future = executor.submit(process_message, *args)
            future.add_done_callback(process_result)
