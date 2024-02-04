# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Pydantic models of acquisition control."""

from pydantic import BaseModel, Extra, Field  # noqa


class ScanJob(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic model definition of a scanjob."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.ignore

    job_id: int = Field(alias="id")
    sequence_id: str
    workflow_id: int
    device_id: str


class ScanStatus(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanjob."""

    record_id: str
    status_percent: int


class ScanRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of data to receive."""

    record_id: str
