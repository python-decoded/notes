import asyncio
import websockets
from websockets.asyncio.server import ServerConnection


async def handler(websocket: ServerConnection):

    print(f"Виконане з'єднання з юрл: {websocket.request.path}")
    await websocket.send("Вітаю, як справи!!!")

    try:
        while True:
            msg = await websocket.recv()
            print(f"Отримане повідомлення '{msg}'")
            await websocket.send("Дякую за повідомлення!")

    except websockets.exceptions.ConnectionClosed:
        print("З'єднання закрите клієнтом")


async def main():
    async with websockets.serve(handler, "0.0.0.0", 5000) as server:
        print("Cервер запущено на порту 5000")
        await server.serve_forever()


asyncio.run(main())
