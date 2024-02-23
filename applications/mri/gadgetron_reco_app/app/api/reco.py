# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Cartesian reco file for the MRI cartesian reco service."""

import logging
import os
from typing import Any

import numpy as np
import pydicom
import pydicom._storage_sopclass_uids
import requests
from pydantic import BaseModel, StrictStr
from pydicom.dataset import Dataset

# from scanhub import RecoJob # type: ignore


EXAM_MANAGER_URI = "host.docker.internal:8004"


class RecoJob(BaseModel):
    """RecoJob is a pydantic model for a reco job."""  # noqa: E501

    record_id: int
    input: StrictStr


# initialize logger
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)


def hello_world(message: Any) -> None:  # pylint: disable=too-many-statements
    """Run the cartesian reco.

    Parameters
    ----------
        message (Any): Message to run the cartesian reco
    """
    log.info("starting cartesian reco with message: %s", message)
    reco_job = RecoJob(**(message.value))
    log.info("reco_job.input: %s", reco_job.input)

    app_filename = f"/app/data_lake/{reco_job.input}"

    log.info("Loading K-Space from %s", app_filename)

    log.info("Hello Gadgetron reco")