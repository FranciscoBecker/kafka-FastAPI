from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schema import Channel, Transmission
from typing import Dict, List
import asyncio
from typing import AsyncGenerator

sse_router = APIRouter()

# Dicionário para armazenar conexões por ID do canal
connections: Dict[int, List[asyncio.Queue]] = {}

# Gerador para transmitir mensagens a um cliente conectado ao sse
async def event_stream(channels: List[Channel]) -> AsyncGenerator[str, None]:
    message_queue = asyncio.Queue()
    for channel in channels:
        if channel.id not in connections:
            connections[channel.id] = []
        connections[channel.id].append(message_queue)
    try:
        while True:
            message = await message_queue.get()  # Aguarda uma nova mensagem
            yield f"data: {message}\n\n"
    finally:
        # Remove a fila ao desconectar
        for channel in channels:
            connections[channel.id].remove(message_queue)
            if not connections[channel.id]:  # Remove a chave se não houver mais conexões
                del connections[channel.id]

@sse_router.get("/sse")
async def sse_endpoint(channels: List[Channel]):
    """Endpoint SSE para clientes se conectarem com um ou mais ID de canal."""
    return StreamingResponse(event_stream(channels), media_type="text/event-stream")

#End point restfull para enviar uma mensagem e um id de canal, todos os clientes conectados para quel id irão receber a mensagem
@sse_router.post("/broadcast/")
async def broadcast(transmissions: List[Transmission]):
    """Envia uma mensagem apenas para os clientes conectados com o ID especificado."""
    for transmission in transmissions:
        if transmission.id_channel in connections:
            for message_queue in connections[transmission.id_channel]:
                await message_queue.put(transmission.message)  # Adiciona a mensagem à fila dos clientes com o ID

    return {"message": f"Mensagem enviada para os clientes."}
