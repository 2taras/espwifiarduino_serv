from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from asyncio import gather

app = FastAPI()

clients = {}

async def send_to_client(client, data):
    try:
        await client.send_text(data)
    except:
        clients[client] == ""

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
                out_tasks = []
                for client, room in clients.items():
                    if(room == clients[websocket] and (clients[websocket] != "" and client != websocket)):
                        out_tasks += [send_to_client(client, data)]
                await gather(*out_tasks)
    except WebSocketDisconnect:
        clients[websocket] = ""