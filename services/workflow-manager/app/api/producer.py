import asyncio
import json
import logging

from aiokafka import AIOKafkaProducer


class Producer:
    """Producer Singleton class for Kafka producer."""

    _instance = None  # Keep instance reference

    def __new__(cls):
        """Create new instance of Producer.

        Returns
        -------
        producer
            Kafka producer
        """
        if cls._instance is None:
            cls._instance = super(Producer, cls).__new__(cls)
            cls._instance.producer = AIOKafkaProducer(
                bootstrap_servers="kafka:9092", value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
        return cls._instance

    async def start(self):
        """Start producer."""
        await self.producer.start()

    async def stop(self):
        """Stop producer."""
        await self.producer.stop()

    async def send(self, topic, message):
        """Send message to Kafka topic.

        Parameters
        ----------
        topic
            Kafka topic to send message to
        message
            Message to be sent
        """
        result = await self.producer.send_and_wait(topic, message)
        return result

    @classmethod
    def get_producer(cls):
        """Get producer."""
        if cls._instance is None:
            cls._instance = Producer()
        return cls._instance  # Return the Singleton instance itself


# Initialize logging
logging.basicConfig(level=logging.INFO)


# Usage example
async def main():
    producer_instance = Producer.get_producer()
    await producer_instance.start()
    await producer_instance.send("my_topic", {"key": "value"})
    await producer_instance.stop()


# Run the example
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
