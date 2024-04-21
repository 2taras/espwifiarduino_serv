from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

clients = {}

@app.websocket("/wss")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients[websocket] = ""
    try:
        while True:
            data = await websocket.receive_text()
            if data.startswith("connect "):
                clients[websocket] = data.split(" ")[1]
            else:
                for client, room in clients.items():
                    if(room == clients[websocket] and (clients[websocket] != "" and client != websocket)):
                        await client.send_text(data)
    except WebSocketDisconnect:
        clients[websocket] = ""