# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Sequence object pydantic models."""

from pydantic import BaseModel


class SequenceIn(BaseModel):
    name: str
    plot: str
    genres: list[str]
    devices_id: list[int]


class SequenceOut(SequenceIn):
    id: int


class SequenceUpdate(SequenceIn):
    name: (str | None)
    plot: (str | None)
    genres: (list[str] | None)
    devices_id: (list[int] | None)
