from fastapi import FastAPI, WebSocket


app = FastAPI()


@app.websocket("/websocket")
async def handler(websocket: WebSocket):

    print("Виконане з'єднання")
    await websocket.accept()
    await websocket.send_text("Вітаю, як справи!!!")

    while True:
        msg = await websocket.receive_text()
        print(f"Отримане повідомлення {msg}")
        await websocket.send_text("Дякую за повідомлення")
