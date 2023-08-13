from settings import settings
import json
from aiokafka import AIOKafkaProducer

def serializer(value):
    return json.dumps(value).encode()

async def produce_event(message, topic):
    producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.broker_host}:{settings.broker_port}",
        value_serializer=serializer
    )
    await producer.start()

    await producer.send_and_wait(topic, value=message)
    await producer.stop()
