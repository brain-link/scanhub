# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Worker file for the MRI cartesian reco service."""

from typing import Set, Any

import logging

from cartesian_reco import cartesian_reco


# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)


def init(message: Any) -> None:
    log.info(f'Initializing worker: {message}')

    # ToDo place your initialization here


def run(message: Any) -> None:
    # do something with the message
    log.info(f'Processing message: {message}')

    # ToDo place your reco here
    cartesian_reco(message)