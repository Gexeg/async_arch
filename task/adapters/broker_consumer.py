import json
from aiokafka import AIOKafkaConsumer
from settings import settings
from commands.process_user_created import process_user_created
from commands.process_user_updated import process_user_updated
from commands.process_user_deleted import process_user_deleted
from utils.logger import LOG

EVENT_PROCESSORS = {
    ("account_streaming", "UserCreated"): process_user_created,
    ("account_streaming", "UserRoleUpdated"): process_user_updated,
    ("account_streaming", "UserDeleted"): process_user_deleted,
}


class KafkaConsumerAsync:
    def __init__(self, topics):
        self.topics = topics
        self.consumer = None

    def deserializer(self, serialized):
        return json.loads(serialized)

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=f"{settings.broker_host}:{settings.broker_port}",
            value_deserializer=self.deserializer,
        )
        await self.consumer.start()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()

    async def consume(self):
        if not self.consumer:
            return

        async for message in self.consumer:
            LOG.debug("Got event %s", message)
            message_data = message.value
            topic = message.topic
            event = message_data["event"]
            processor = EVENT_PROCESSORS.get((topic, event))
            LOG.debug(
                "Got processor %s by topic %s type %s and event %s",
                processor,
                topic,
                type(topic),
                event,
            )
            if processor:
                await processor(message_data["data"])


consumer = KafkaConsumerAsync(topics=["account_streaming", "account"])
