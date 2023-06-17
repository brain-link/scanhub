# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Acquisition control. Receives control cmd from ui and controls scans on devices."""

#  python -m uvicorn acquisitioncontrol:app --reload

import json
import logging
import random

import requests
from fastapi import FastAPI
from pydantic import BaseModel, Extra, Field

DEBUG_FLAG = True

# DEVICE_URI = "host.docker.internal:8001"
DEVICE_URI = "host.docker.internal:5000"
SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "host.docker.internal:8004"


# TODO: Move to scanhub-tools/models file


class ScanJob(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic model definition of a scanjob."""

    class Config:
        """Pydantic configuration."""

        extra = Extra.ignore

    job_id: int = Field(alias="id")
    sequence_id: str
    workflow_id: int
    device_id: int


# TODO: Move to scanhub-tools
class ScanStatus(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanjob."""

    record_id: str
    status_percent: int


# TODO: Move to scanhub-tools
class ScanRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of data to receive."""

    record_id: str


app = FastAPI(
    openapi_url="/api/v1/mri/acquisitioncontrol/openapi.json",
    docs_url="/api/v1/mri/acquisitioncontrol/docs",
)
logging.basicConfig(level=logging.DEBUG)


@app.post("/api/v1/mri/acquisitioncontrol/start-scan")
async def start_scan(scan_job: ScanJob):
    """Receives a job. Create a record id, trigger scan with it and returns it."""
    if DEBUG_FLAG is True:

        # TODO: Dont ignore device_id, check returns, ...

        record_id = "test_" + str(random.randint(0, 1000))
        sequence_json = {"test": "test"}

        url = f"http://{DEVICE_URI}/api/start-scan"
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
        # get sequence
        res = requests.get(
            f"http://{SEQUENCE_MANAGER_URI}/api/v1/mri/sequences/{scan_job.sequence_id}",
            timeout=60,
        )
        sequence_json = res.json()

        # create record
        # TODO: data_path, comment ?
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
        print(sequence_json)

        url = f"http://{DEVICE_URI}/api/start-scan"
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


@app.post("/api/v1/mri/acquisitioncontrol/forward-status")
async def forward_status(scan_status: ScanStatus):
    """Receives status for a job. Forwards it to the ui and returns ok."""
    print("Received status: %s", scan_status)
    return {"message": "Status submitted"}
