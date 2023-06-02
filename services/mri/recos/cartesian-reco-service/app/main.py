# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Main file for the MRI cartesian reco service."""

from random import randint
from typing import Set, Any
from fastapi import FastAPI
from kafka import TopicPartition

import aiokafka
import asyncio
import json
import logging
import os

from worker import init, run


# instantiate the API
app = FastAPI()

# global variables
consumer_task = None
consumer = None

# env variables
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC_SUBSCRIPTION')
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv('KAFKA_CONSUMER_GROUP_PREFIX', 'group')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka-broker:9093')

# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    log.info('Initializing API ...')
    await initialize()
    await consume()


@app.on_event("shutdown")
async def shutdown_event():
    log.info('Shutting down API')
    consumer_task.cancel()
    await consumer.stop()


@app.get("/")
async def root():
    return {"message": "Cartesian Reco Service"}


async def initialize():
    loop = asyncio.get_event_loop()
    global consumer
    group_id = f'{KAFKA_CONSUMER_GROUP_PREFIX}-{randint(0, 10000)}'
    log.debug(f'Initializing KafkaConsumer for topic {KAFKA_TOPIC}, group_id {group_id}'
              f' and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}')
    consumer = aiokafka.AIOKafkaConsumer(KAFKA_TOPIC, loop=loop,
                                         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                         group_id=group_id,
                                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    # get cluster layout and join group
    await consumer.start()

    partitions: Set[TopicPartition] = consumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        log.warning(f'Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. Expecting '
                    f'only one, remaining partitions will be ignored!')
    for tp in partitions:

        # get the log_end_offset
        end_offset_dict = await consumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPIC}) has no messages (log_end_offset: '
                        f'{end_offset}), skipping initialization ...')
            return

        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset-1}')
        consumer.seek(tp, end_offset-1)
        msg = await consumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')

        # run worker initialization
        init(msg)
        return


async def consume():
    global consumer_task
    consumer_task = asyncio.create_task(send_consumer_message(consumer))


async def send_consumer_message(consumer):
    try:
        # consume messages
        async for msg in consumer:
            # x = json.loads(msg.value)
            log.info(f"Consumed msg: {msg}")

            # run worker
            run(msg)
    finally:
        # will leave consumer group; perform autocommit if enabled
        log.warning('Stopping consumer')
        await consumer.stop()
