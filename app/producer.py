from aiokafka import AIOKafkaProducer
from schema import Message
from config import loop, KAFKA_TOPIC, KAFKA_BOOTSTRAT_SERVERS, KAFKA_CONSUMER_GROUP
import json

async def send_message(message: Message):
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAT_SERVERS)
    await producer.start()
    try:
        print(f'Enviando mensagem com valor: {message}')
        value_json = json.dumps(message.__dict__).encode('utf-8')
        await producer.send_and_wait(topic=KAFKA_TOPIC, value=value_json)
    finally:
        await producer.stop()