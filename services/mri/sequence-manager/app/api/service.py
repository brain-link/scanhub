# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Service file for the MRI sequence manager service."""

import os
import httpx

DEVICE_SERVICE_HOST_URL = 'http://localhost:8002/api/v1/devices/'

def is_device_present(device_id: int):
    url = os.environ.get('DEVICE_SERVICE_HOST_URL') or DEVICE_SERVICE_HOST_URL
    r = httpx.get(f'{url}{device_id}')
    return True if r.status_code == 200 else False