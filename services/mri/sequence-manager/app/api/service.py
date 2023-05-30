#!/usr/bin/env python3

# Project: ScanHub
# File: service.py
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
# Brief: Service file for the MRI sequence manager service.

import os
import httpx

DEVICE_SERVICE_HOST_URL = 'http://localhost:8002/api/v1/devices/'

def is_device_present(device_id: int):
    url = os.environ.get('DEVICE_SERVICE_HOST_URL') or DEVICE_SERVICE_HOST_URL
    r = httpx.get(f'{url}{device_id}')
    return True if r.status_code == 200 else False