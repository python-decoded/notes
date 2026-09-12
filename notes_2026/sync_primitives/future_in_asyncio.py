
import asyncio


async def deliver_pizza():
    await asyncio.sleep(10)
    return "PEPERONI"


async def main():
    deliver_pizza_coro = deliver_pizza()
    task = asyncio.create_task(deliver_pizza_coro)
    await task
    my_pizza = task.result()
    print(f"My pizza is {my_pizza}")


if __name__ == '__main__':
    asyncio.run(main())





