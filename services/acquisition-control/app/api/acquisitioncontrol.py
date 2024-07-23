# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Acquisition control. Receives control cmd from ui and controls scans on devices."""
# pylint: disable=no-name-in-module
# pylint: disable=too-many-statements
# python -m uvicorn acquisitioncontrol:app --reload

import json
import logging
from enum import Enum
from xml.etree.ElementTree import Element, SubElement, tostring

import httpx
from defusedxml import lxml as dlxml
from fastapi import APIRouter
from lxml import etree
from pydantic import BaseModel
from pydantic.json import pydantic_encoder
from scanhub_libraries.models import ScanStatus
from scanhub_libraries.scan_task_models import Commands, DeviceTask, ISMRMRDHeader, UserParametersString

SEQUENCE_MANAGER_URI = "host.docker.internal:8003"
EXAM_MANAGER_URI = "host.docker.internal:8004"

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)


# Namespaces
ns = {
    'ismrmrd': 'http://www.ismrm.org/ISMRMRD',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}


def pydantic_to_xml(element: Element, obj: BaseModel):
    """Convert a Pydantic model to XML format recursively."""
    for field, value in obj:
        if isinstance(value, BaseModel):
            sub_element = SubElement(element, field)
            pydantic_to_xml(sub_element, value)
        elif isinstance(value, list):
            for item in value:
                sub_element = SubElement(element, field)
                if isinstance(item, BaseModel):
                    pydantic_to_xml(sub_element, item)
                else:
                    sub_element.text = str(item)
        elif isinstance(value, Enum):
            sub_element = SubElement(element, field)
            sub_element.text = value.value
        else:
            sub_element = SubElement(element, field)
            sub_element.text = str(value)

def generate_xml_from_model(model: ISMRMRDHeader):
    """Generate an XML string from the Pydantic model."""
    # mypy errors has to be ignored due to special character in key of **extra
    root = Element('ismrmrdHeader', xmlns=ns['ismrmrd'], **{'xmlns:xsi': ns['xsi']}) # type: ignore[arg-type]
    pydantic_to_xml(root, model)
    return tostring(root, encoding='unicode')



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
            "job_id": str(job_id),
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
        response = await client.post(url, content=data)
        return response.status_code


@router.post("/start-scan")
async def start_scan(scan_job: ISMRMRDHeader):
    """Receives a job. Create a record id, trigger scan with it and returns it."""
    device_id = scan_job.acquisitionSystemInformation.deviceID
    record_id = ""
    command = Commands.START

    device_ip = await device_location_request(device_id)
    url = f"http://{device_ip}/api/start-scan"

    print("Start-scan endpoint, device ip: ", device_ip)

    # get sequence
    sequence_json = await retrieve_sequence(SEQUENCE_MANAGER_URI, scan_job.measurementInformation.sequenceName)

    # create record
    record_id = "blub" # await create_record(EXAM_MANAGER_URI, scan_job.measurementInformation.measurementID)
    scan_job.userParameters.userParameterString.append(UserParametersString(name="record_id", value=record_id))

    # start scan and forward sequence, workflow, record_id
    logging.debug("Received job: %s, Generated record id: %s", scan_job.measurementInformation.measurementID, record_id)



    xml_data = generate_xml_from_model(scan_job)

    xsd_path = "ismrmrd.xsd"
    schema = etree.XMLSchema(file=xsd_path)
    parser = etree.XMLParser(schema = schema)
    ___ = dlxml.fromstring(xml_data, parser)

    # fill record id
    print(sequence_json)
    device_task = DeviceTask(
        ismrmrd_header=xml_data, command=command, sequence=sequence_json["file"]
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
