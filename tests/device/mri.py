"""Module providingFunction simulating a device with scancontrol."""
import os
import logging

from fastapi import FastAPI
from pydantic import BaseModel  # pylint: disable=no-name-in-module
import requests


URL_ACQ_CTRL = os.getenv("SCANHUB_URL_ACQ_CTRL", "")
RECORDS_PATH = "./records/"


class ScanRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of data to receive"""
    record_id: str


logging.basicConfig(level=logging.DEBUG)
app = FastAPI()


@app.post("/start-scan")
async def root(scan_request: ScanRequest):
    """Endpoint to trigger a scan."""
    sequence = ""
    with open(f"{RECORDS_PATH}{scan_request.record_id}/sequence",
              "r", encoding='UTF-8') as sequence_file:
        sequence = sequence_file.read()
    logging.debug("Loaded sequence: %s", sequence)
    pre_scan()
    start_scan()
    post_scan()
    return {"message": f"""Scanrequest {scan_request.record_id} received.
      Scan is scheduled."""}


def simulate_scan():
    """simulates a scan"""
    # TODO: This is just for debug purposes
    return


def start_scan():
    """do something to start the scan"""
    simulate_scan()
    return


def pre_scan():
    """steps to do before the scan is executed"""
    return


def post_scan():
    """steps to do after the scan was executed"""
    return


def upload_image(record_id):
    """upload the image to acq control"""
    try:
        file_handler = open(f"{RECORDS_PATH}{record_id}/result",
                            "r", encoding='UTF-8')
    except Exception as ex:  # pylint: disable=broad-exception-caught
        print(ex)
        return False

    file = {'file': file_handler}
    url = f"{URL_ACQ_CTRL}"  # TODO: complete url

    try:
        requests.post(url, files=file, timeout=10)
    except Exception as ex:  # pylint: disable=broad-exception-caught
        print(ex)
        file_handler.close()
        return False

    file_handler.close()
    return


def submit_status(record_id, percentage):
    """submit status to acq_control"""
    # TODO: Call endpoint on acq control
    return
