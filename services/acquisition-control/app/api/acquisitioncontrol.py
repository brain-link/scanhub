# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Acquisition control. Receives control cmd from ui and controls scans on devices."""
# pylint: disable=no-name-in-module
# pylint: disable=too-many-statements
# python -m uvicorn acquisitioncontrol:app --reload

import json
import logging
import random

import httpx
from fastapi import APIRouter
from pydantic.json import pydantic_encoder

from scanhub_libraries.models import Commands, DeviceTask, ParametrizedSequence, ScanJob, ScanStatus

DEBUG_FLAG = False

SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "host.docker.internal:8004"

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)


async def device_location_request(device_id):
    """Retrieve ip from device-manager.

    Parameters
    ----------
    device_id
        Id of device

    Returns
    -------
        ip_address of device
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api-gateway:8080/api/v1/device/{device_id}/ip_address")
        return response.json()["ip_address"]


async def retrieve_sequence(sequence_manager_uri, sequence_id):
    """Retrieve sequence and sequence-type from sequence-manager.

    Parameters
    ----------
    sequence_manager_uri
        uri of sequence manager

    sequence_id
        id of sequence

    Returns
    -------
        sequence
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://{sequence_manager_uri}/api/v1/mri/sequences/{sequence_id}")
        return response.json()


async def create_record(exam_manager_uri, job_id):
    """Create new record at exam_manager and retrieve record_id.

    Parameters
    ----------
    exam_manager_uri
        uri of sequence manager

    job_id
        id of job

    Returns
    -------
        id of newly created record
    """
    async with httpx.AsyncClient() as client:
        # TODO: data_path, comment ? # pylint: disable=fixme
        data = {
            "data_path": "unknown",
            "comment": "Created in Acquisition Control",
            "job_id": job_id,
        }
        response = await client.post(f"http://{exam_manager_uri}/api/v1/exam/record", json=data)
        return response.json()["id"]


async def post_device_task(url, device_task):
    """Send task do device.

    Parameters
    ----------
    url
        url of the device

    device_task
        task

    Returns
    -------
        response of device
    """
    async with httpx.AsyncClient() as client:
        data = json.dumps(device_task, default=pydantic_encoder)
        response = await client.post(url, data=data)
        return response.status_code


@router.post("/start-scan")
async def start_scan(scan_job: ScanJob):
    """Receives a job. Create a record id, trigger scan with it and returns it."""
    device_id = scan_job.device_id
    record_id = ""
    command = Commands.START

    device_ip = await device_location_request(device_id)
    url = f"http://{device_ip}/api/start-scan"

    if DEBUG_FLAG is True:
        # TODO: Dont ignore device_id, check returns, ... # pylint: disable=fixme
        record_id = "test_" + str(random.randint(0, 1000))
        sequence_json = {"test": "test"}
        parametrized_sequence = ParametrizedSequence(
            acquisition_limits=scan_job.acquisition_limits,
            sequence_parameters=scan_job.sequence_parameters,
            sequence=sequence_json,
        )
    else:
        print("Start-scan endpoint, device ip: ", device_ip)
        # get sequence
        sequence_json = await retrieve_sequence(SEQUENCE_MANAGER_URI, scan_job.sequence_id)

        # create record
        record_id = await create_record(EXAM_MANAGER_URI, scan_job.job_id)
        parametrized_sequence = ParametrizedSequence(
            acquisition_limits=scan_job.acquisition_limits,
            sequence_parameters=scan_job.sequence_parameters,
            sequence=json.dumps(sequence_json),
        )

    # start scan and forward sequence, workflow, record_id
    logging.debug("Received job: %s, Generated record id: %s", scan_job.job_id, record_id)

    device_task = DeviceTask(
        device_id=device_id, record_id=record_id, command=command, parametrized_sequence=parametrized_sequence
    )
    status_code = await post_device_task(url, device_task)

    if status_code == 200:
        print("Scan started successfully.")
    else:
        print("Failed to start scan.")
    return {"record_id": record_id}


@router.post("/forward-status")
async def forward_status(scan_status: ScanStatus):
    """Receives status for a job. Forwards it to the ui and returns ok."""
    print("Received status: %s", scan_status)
    return {"message": "Status submitted"}
