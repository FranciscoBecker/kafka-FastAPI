from time import sleep

from websocket_connection_manager import ConnectionManager
from config import loop, KAFKA_TOPIC, KAFKA_BOOTSTRAT_SERVERS, KAFKA_CONSUMER_GROUP
from aiokafka import AIOKafkaConsumer

consumer_manager = ConnectionManager()

async def consumer():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAT_SERVERS,
                                group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumindo mensagem: {msg}')
            await consumer_manager.broadcast(f"Client said: {msg}")
    finally:
        await consumer.stop()

