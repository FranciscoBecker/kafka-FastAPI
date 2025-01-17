from config import loop, KAFKA_TOPIC, KAFKA_BOOTSTRAT_SERVERS, KAFKA_CONSUMER_GROUP
from aiokafka import AIOKafkaConsumer

async def consumer():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAT_SERVERS,
                                group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumindo mensagem: {msg}')
    finally:
        await consumer.stop()