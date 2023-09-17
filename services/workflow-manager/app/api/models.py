# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Workflow object pydantic models."""

from datetime import datetime

from pydantic import BaseModel

from .db import Workflow


class BaseWorkflow(BaseModel):
    """Workflow pydantic base model."""

    name: str
    description: (str | None)
    version: str
    author: (str | None)

class WorkflowIn(BaseWorkflow):
    """Workflow pydantic output model."""

    definition: dict

class WorkflowMetaOut(BaseWorkflow):
    """Workflow pydantic output model."""

    id: int  # TBD: Use uuid
    datetime_created: datetime
    datetime_updated: (datetime | None)

class WorkflowOut(WorkflowMetaOut):
    """Workflow pydantic output model."""

    definition: dict


async def get_workflow_meta_out(data: Workflow) -> WorkflowMetaOut:
    """Workflow pydantic output model helper function.

    Parameters
    ----------
    data
        Database ORM model

    Returns
    -------
        Pydantic output model
    """
    return WorkflowMetaOut(
        id=data.id,
        name=data.name,
        description=data.description,
        version=data.version,
        author=data.author,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
    )

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
        name=data.name,
        description=data.description,
        version=data.version,
        author=data.author,
        definition=data.definition,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
    )
