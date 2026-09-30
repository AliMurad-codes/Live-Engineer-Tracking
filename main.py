from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List


app = FastAPI(
    title="Live Engineer Tracking API"
)


# Store all connected dashboard/engineer clients
connected_clients: List[WebSocket] = []


@app.get("/")
def home():
    return {
        "message": "Live Engineer Tracking API is running"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    connected_clients.append(websocket)

    print("Client connected")
    print("Connected clients:", len(connected_clients))

    try:

        while True:

            # Receive message from engineer
            data = await websocket.receive_json()

            print("Location received:")
            print(data)

            # Broadcast location to every connected client
            for client in connected_clients:

                await client.send_json(data)

    except WebSocketDisconnect:

        connected_clients.remove(websocket)

        print("Client disconnected")
        print("Connected clients:", len(connected_clients))