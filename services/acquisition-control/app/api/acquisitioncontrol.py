# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Acquisition control. Receives control cmd from ui and controls scans on devices."""
# pylint: disable=no-name-in-module
# pylint: disable=too-many-statements
# python -m uvicorn acquisitioncontrol:app --reload

import json
import logging
import random

import requests
import httpx
from fastapi import APIRouter
from .models import ScanJob, ScanStatus


DEBUG_FLAG = False

SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "host.docker.internal:8004"

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)


async def device_location_request(device_id):
    """Retrieve ip from device-manager."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api-gateway:8080/api/v1/device/{device_id}/ip_address")
        return response.json()["ip_address"]


@router.post("/start-scan")
async def start_scan(scan_job: ScanJob):
    """Receives a job. Create a record id, trigger scan with it and returns it."""
    device_ip = await device_location_request(scan_job.device_id)
    
    if DEBUG_FLAG is True:
        # TODO: Dont ignore device_id, check returns, ... # pylint: disable=fixme

        record_id = "test_" + str(random.randint(0, 1000))
        sequence_json = {"test": "test"}

        url = f"http://{device_ip}/api/start-scan"
        print(url)
        response = requests.post(
            url,
            json={"record_id": record_id, "sequence": json.dumps(sequence_json)},
            timeout=60,
        )

        if response.status_code == 200:
            print("Scan started successfully.")
        else:
            print("Failed to start scan.")

    else:
        print("Start-scan endpoint, device ip: ", device_ip)
        # get sequence
        res = requests.get(
            f"http://{SEQUENCE_MANAGER_URI}/api/v1/mri/sequences/{scan_job.sequence_id}",
            timeout=60,
        )
        sequence_json = res.json()

        # create record
        # TODO: data_path, comment ? # pylint: disable=fixme
        res = requests.post(
            f"http://{EXAM_MANAGER_URI}/api/v1/exam/record",
            json={"data_path": "path", "comment": "blub", "job_id": scan_job.job_id},
            timeout=60,
        )
        record_id = res.json()["id"]

        # start scan and forward sequence, workflow, record_id
        logging.debug(
            "Received job: %s, Generated record id: %s", scan_job.job_id, record_id
        )
        # print(sequence_json)

        print("RECORD: ", res.json())

        url = f"http://{device_ip}/api/start-scan"
        print(url)
        response = requests.post(
            url,
            json={"record_id": record_id, "sequence": json.dumps(sequence_json)},
            timeout=60,
        )

        if response.status_code == 200:
            print("Scan started successfully.")
        else:
            print("Failed to start scan.")

    print(response)
    return {"record_id": record_id}


@router.post("/forward-status")
async def forward_status(scan_status: ScanStatus):
    """Receives status for a job. Forwards it to the ui and returns ok."""
    print("Received status: %s", scan_status)
    return {"message": "Status submitted"}
