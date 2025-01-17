from fastapi import FastAPI
import router, websocket_router
import asyncio
import consumer

app = FastAPI()


@app.get('/')
async def home():
    return 'welcome home'


app.include_router(router.router)
app.include_router(websocket_router.websocket_router)
asyncio.create_task(consumer.consumer())