# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Main file for the MRI cartesian reco service."""

import asyncio
import json
import logging
import os
from random import randint
from typing import Set

from aiokafka import AIOKafkaConsumer  # type: ignore
from fastapi import FastAPI
from kafka import TopicPartition  # type: ignore
from kafka.errors import GroupCoordinatorNotAvailableError, KafkaConnectionError, NoBrokersAvailable  # type: ignore

from api.worker import init, run

# instantiate the API
app = FastAPI()

# global variables
CONSUMER_TASK = None
CONSUMER = None

# env variables
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC_SUBSCRIPTION")
KAFKA_CONSUMER_GROUP_PREFIX = os.getenv("KAFKA_CONSUMER_GROUP_PREFIX", "group")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

# initialize logger
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    """Startup event for the API."""
    log.info("Initializing API ...")
    await initialize()
    await consume()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for the API."""
    log.info("Shutting down API")
    CONSUMER_TASK.cancel()
    await CONSUMER.stop()


@app.get("/")
async def root():
    """Root endpoint for the API."""
    return {"message": "Cartesian Reco Service"}


async def initialize():
    """Initialize the API."""
    loop = asyncio.get_event_loop()
    global CONSUMER # pylint: disable=global-statement
    group_id = f"{KAFKA_CONSUMER_GROUP_PREFIX}-{randint(0, 10000)}" # noqa: S311
    # pylint: disable=logging-fstring-interpolation
    log.debug(
        f"Initializing KafkaConsumer for topic {KAFKA_TOPIC}, group_id "
        f"{group_id} and using bootstrap servers {KAFKA_BOOTSTRAP_SERVERS}"
    )

    retries = 5
    for i in range(retries):
        try:
            CONSUMER = AIOKafkaConsumer(
                KAFKA_TOPIC,
                loop=loop,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                group_id=group_id,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
            )
            await CONSUMER.start()
            break
        except NoBrokersAvailable:
            print("Brokers not available yet. Retrying...")
            await asyncio.sleep(5)
        except KafkaConnectionError:
            print(f"Attempt {i+1}: Could not connect. Retrying...")
            await asyncio.sleep(5)
        except GroupCoordinatorNotAvailableError:
            print(f"Attempt {i+1}: Group Coordinator not available. Retrying...")
            await asyncio.sleep(5)

    # get cluster layout and join group
    partitions: Set[TopicPartition] = CONSUMER.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        # pylint: disable=logging-fstring-interpolation
        log.warning(
            f"Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. "
            f"Expecting only one, remaining partitions will be ignored!"
        )
    for topic in partitions:
        # get the log_end_offset
        end_offset_dict = await CONSUMER.end_offsets([topic])
        end_offset = end_offset_dict[topic]

        if end_offset == 0:
            # pylint: disable=logging-fstring-interpolation
            log.warning(
                f"Topic {KAFKA_TOPIC} has no messages (log_end_offset: " f"{end_offset}), skipping initialization ..."
            )
            return

        # pylint: disable=logging-fstring-interpolation
        log.debug(f"Found log_end_offset: {end_offset} seeking to {end_offset - 1}")
        CONSUMER.seek(topic, end_offset - 1)
        msg = await CONSUMER.getone()
        log.info("Initializing API with data from msg: %s", msg)

        # run worker initialization
        init(msg)
        return


async def consume():
    """Consume messages from the Kafka topic."""
    global CONSUMER_TASK # pylint: disable=global-statement
    CONSUMER_TASK = asyncio.create_task(send_consumer_message(CONSUMER))


async def send_consumer_message(consumer):
    """Send consumer message to the worker.

    Parameters
    ----------
        consumer (AIOKafkaConsumer): Kafka consumer
    """
    try:
        async for msg in consumer:
            log.info("Consumed msg: %s", msg)
            # run worker
            run(msg)
    finally:
        log.warning("Stopping consumer")
        await consumer.stop()
