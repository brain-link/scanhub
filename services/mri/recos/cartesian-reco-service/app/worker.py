# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Worker file for the MRI cartesian reco service."""

import logging
from typing import Any

from .reco import cartesian_reco

# initialize logger
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
log = logging.getLogger(__name__)


def init(message: Any) -> None:
    """Initialize the worker.

    Parameters
    ----------
        message (Any): Message to initialize the worker
    """
    log.info("Initializing worker: %s", message)

    # place your initialization here


def run(message: Any) -> None:
    """Run the worker.

    Parameters
    ----------
        message (Any): Message to run the worker
    """

    # do something with the message
    log.info("Processing message: %s", message)

    # place your reco here
    cartesian_reco(message)
