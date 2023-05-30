#!/usr/bin/env python3

# Project: ScanHub
# File: models.py
# Date: June 2023
#
# License:
# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
#
# SPDX-License-Identifier: GPL-3.0-only OR ScanHub commercial license
#
# Licensees holding valid ScanHub commercial licenses may use this file in
# accordance with the ScanHub Commercial License Agreement provided with the
# Software or, alternatively, in accordance with the GPL-3.0-only as published
# by the Free Software Foundation. Please refer to the License for the
# specific language governing the rights and limitations under either license.
#
# Brief: Workflow object pydantic models.

from datetime import datetime

from api.db import Workflow
from pydantic import BaseModel


class BaseWorkflow(BaseModel):
    """Workflow pydantic base model."""

    host: str
    name: str
    author: (str | None)
    modality: str
    type: str
    status: str
    kafka_topic: str


class WorkflowOut(BaseWorkflow):
    """Workflow pydantic output model."""

    # TODO: Use uuid as id instead of id
    id: int
    datetime_created: datetime
    datetime_updated: (datetime | None)


async def get_workflow_out(data: Workflow) -> WorkflowOut:
    """Workflow pydantic output model helper function.

    Parameters
    ----------
    data
        Database ORM model

    Returns
    -------
        Pydantic output model
    """
    return WorkflowOut(
        id=data.id,
        host=data.host,
        name=data.name,
        author=data.author,
        modality=data.modality,
        type=data.type,
        status=data.status,
        kafka_topic=data.kafka_topic,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
    )
