from fastapi import APIRouter
from schema import Message
from config import loop, KAFKA_TOPIC, KAFKA_BOOTSTRAT_SERVERS, KAFKA_CONSUMER_GROUP
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json

route = APIRouter()


@route.post('/create_message')
async def send(message: Message):
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAT_SERVERS)
    await producer.start()
    try:
        print(f'Enviando mensagem com valor: {message}')
        value_json = json.dumps(message.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
    finally:
        await producer.stop()

async def consumer():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC,loop=loop,bootstrap_servers=KAFKA_BOOTSTRAT_SERVERS,group_id=KAFKA_CONSUMER_GROUP)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumindo mensagem: {msg}')
    finally:
        await consumer.stop()