from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from websocket_connection_manager import ConnectionManager
from consumer import consumer_manager

websocket_router = APIRouter()

manager = ConnectionManager()


@websocket_router.websocket("/websocket")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")
    try:
        while True:
            # Aguarda mensagem do cliente
            message = await websocket.receive_text()
            print(f"Message received: {message}")

            # Envia uma resposta de volta ao cliente
            await websocket.send_text(f"Server received: {message}")
    except Exception as e:
        print(f"Connection closed: {e}")


@websocket_router.websocket("/ws-all")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Recebe mensagem do cliente
            data = await websocket.receive_text()
            # Envia a mensagem para todos os clientes conectados
            await manager.broadcast(f"Client said: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")


@websocket_router.websocket("/ws-consumer")
async def websocket_endpoint(websocket: WebSocket):
    await consumer_manager.connect(websocket)
    try:
        while True:
            print("client connected")
            await websocket.send_text(f"Client connect on consumer")
            # Mantém a conexão aberta
            await websocket.receive_text()
            # Mantém a conexão aberta, mas não espera mensagens do front
            #await asyncio.sleep(10)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")
