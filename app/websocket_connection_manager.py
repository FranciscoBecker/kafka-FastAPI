from fastapi import WebSocket

# Gerenciador de conexões ativas
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        disconnected_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Erro ao enviar mensagem para conexão {connection}: {e}")
                disconnected_connections.append(connection)

        # Remove as conexões desconectadas
        for connection in disconnected_connections:
            self.disconnect(connection)