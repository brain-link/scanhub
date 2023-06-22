# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow object pydantic models."""

from datetime import datetime

from pydantic import BaseModel

from .db import Workflow


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

    id: int  # TBD: Use uuid
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
