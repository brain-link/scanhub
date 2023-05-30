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
# Brief: Sequence object pydantic models.

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