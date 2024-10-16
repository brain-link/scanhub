############################################
# Option 1
############################################

from aiokafka import AIOKafkaConsumer
import asyncio
import os
import json

# env variables
KAFKA_TOPIC = 'timestamp'#os.getenv('KAFKA_TOPIC')
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# global variables
loop = asyncio.get_event_loop()


async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                group_id=KAFKA_CONSUMER_GROUP,
                                value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    # get cluster layout and join group KAFKA_CONSUMER_GROUP
    await consumer.start()
    try:
        # consume messages
        async for msg in consumer:
            print(f"Consumed msg: {msg}")
    finally:
        # will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

loop.run_until_complete(consume())


############################################
# Option 2
############################################

# from kafka import KafkaConsumer
# import json

# from TimestampEvent import TimestampEvent

# consumer = KafkaConsumer('timestamp',
#                          value_deserializer=lambda x: json.loads(x.decode('utf-8')),
#                          bootstrap_servers=['localhost:9092'])

# for message in consumer:
#     timestampEvent = TimestampEvent(**(message.value))
#     print("Received: " + timestampEvent.timestamp)
