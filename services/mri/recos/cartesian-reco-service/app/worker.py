#!/usr/bin/env python3

# Project: ScanHub
# File: worker.py
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
# Brief: Worker file for the MRI cartesian reco service.

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