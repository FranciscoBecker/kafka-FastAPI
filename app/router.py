from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from schema import Message
from producer import send_message

router = APIRouter()


@router.post('/create_message')
async def send(message: Message):
    await send_message(message)
    return {"Message: Mensagem enviada com sucesso"}
