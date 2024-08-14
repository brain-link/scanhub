###############################################
# Option 1
# This is a simple producer that sends a timestamp to the topic "timestamp" every 5 seconds.
###############################################

import json
from kafka import KafkaProducer
from datetime import datetime
from time import sleep

from TimestampEvent import TimestampEvent

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x.__dict__).encode('utf-8'))

while True:
    timestampEvent = TimestampEvent(datetime.now().strftime("%H:%M:%S"))
    print("Sending: " + timestampEvent.timestamp)
    producer.send('timestamp', timestampEvent)
    sleep(5)

###############################################
# Option 2
#
# from aiokafka import AIOKafkaProducer
# import asyncio
# import json
# import os
# from random import randint


# # env variables
# KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
# KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# # global variables
# loop = asyncio.get_event_loop()


# async def send_one():
#     producer = AIOKafkaProducer(loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
#     # get cluster layout and initial topic/partition leadership information
#     await producer.start()
#     try:
#         # produce message
#         msg_id = f'{randint(1, 10000)}'
#         value = {'message_id': msg_id, 'text': 'some text', 'state': randint(1, 100)}
#         print(f'Sending message with value: {value}')
#         value_json = json.dumps(value).encode('utf-8')
#         await producer.send_and_wait(KAFKA_TOPIC, value_json)
#     finally:
#         # wait for all pending messages to be delivered or expire.
#         await producer.stop()

# # send message
# loop.run_until_complete(send_one())

