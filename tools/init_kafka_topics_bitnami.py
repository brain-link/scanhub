# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Init kafka topics."""

from kafka.admin import KafkaAdminClient, NewTopic
import logging
logger = logging.getLogger('kafka')
logger.setLevel(logging.DEBUG)


admin_client = KafkaAdminClient(
    bootstrap_servers="localhost:9094", 
    client_id='test',
    security_protocol = 'PLAINTEXT',
    sasl_mechanism = 'PLAIN',
    sasl_plain_username = 'user',
    sasl_plain_password = 'bitnami'
)

topic_list = []
topic_list.append(NewTopic(name="example_topic", num_partitions=1, replication_factor=1))
admin_client.create_topics(new_topics=topic_list, validate_only=False)
