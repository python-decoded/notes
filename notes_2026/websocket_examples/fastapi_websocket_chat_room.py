# fastapi dev fastapi_websocket_chat_room.py


from fastapi import FastAPI, WebSocket, WebSocketDisconnect

messages: list[str] = []
connections: dict[str, list[WebSocket]] = {}

app = FastAPI()

@app.websocket("/websocket/{user_name}")
async def handler(websocket: WebSocket, user_name: str):

    print("Виконане з'єднання")
    await websocket.accept()
    connections.setdefault(user_name, []).append(websocket)

    for msg in messages:
        await websocket.send_text(msg)

    try:
        while True:
            msg = await websocket.receive_text()
            print(f"Отримане повідомлення {msg}")
            messages.append(f"{user_name}: {msg}")

            for websockets in connections.values():
                for _websocket in websockets:
                    if _websocket is not websocket:
                        await _websocket.send_text(f"{user_name}: {msg}")
    except WebSocketDisconnect:
        connections[user_name].remove(websocket)
        if len(connections[user_name]) == 0:
            del connections[user_name]
