# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Sequence object pydantic models."""

from pydantic import BaseModel
from typing import List, Optional

class SequenceIn(BaseModel):
    name: str
    plot: str
    genres: List[str]
    devices_id: List[int]


class SequenceOut(SequenceIn):
    id: int


class SequenceUpdate(SequenceIn):
    name: Optional[str] = None
    plot: Optional[str] = None
    genres: Optional[List[str]] = None
    devices_id: Optional[List[int]] = None