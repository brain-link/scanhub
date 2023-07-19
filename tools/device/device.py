# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Framework to connect a device to brain-links scanhub"""
#  python -m uvicorn mri:app --reload
from abc import ABC, abstractmethod
import logging
import os
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, Json
import requests

# TODO: Move to scanhub-tools
class ScanRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of data to receive"""
    record_id: str
    sequence: Json

# router = InferringRouter()

# @cbv(router)
class Device(ABC):
    """abstract device base class"""
    url_acq_ctrl = ""
    records_path = ""

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, url_acq_ctrl, records_path, app):
        self.url_acq_ctrl = url_acq_ctrl
        self.records_path = records_path
        self.router = APIRouter()
        self.router.add_api_route("/start-scan", self.trigger_scan, methods=["POST"])
        app.include_router(self.router)

    @staticmethod
    @abstractmethod
    def start_scan(scan_request, records_path):
        """do something to start the scan"""

    @staticmethod
    @abstractmethod
    def pre_scan(scan_request):
        """steps to do before the scan is executed"""

    @staticmethod
    @abstractmethod
    def post_scan(scan_request):
        """steps to do after the scan was executed"""  

    def scan_process(self, scan_request: ScanRequest):
        """definition of the scan process. is triggered and runs in the background"""
        self.pre_scan(scan_request)
        self.start_scan(scan_request, self.records_path)
        self.post_scan(scan_request)

    async def trigger_scan(self, scan_request: ScanRequest, background_tasks: BackgroundTasks):
        """Endpoint to trigger a scan."""
        # TODO: multiple device handling
        # TODO: verify that device is not busy. (scheduling, queue, ...)
        seq_file = f"{self.records_path}{scan_request.record_id}\\sequence"
        os.makedirs(os.path.dirname(seq_file), exist_ok=True)
        sequence = scan_request.sequence["file"]
        with open(seq_file, "w", encoding='UTF-8') as sequence_file:
            sequence_file.write(sequence)
        background_tasks.add_task(self.scan_process, scan_request)
        return {"message": f"""Scanrequest {scan_request.record_id} received.
        Scan is scheduled."""}

    def upload_image(self, record_id):
        """upload the image to acq control"""
        try:
            with open(f"{self.records_path}{record_id}/result",
                                "r", encoding='UTF-8') as file_handler:
                file = {'file': file_handler}
                url = f"{self.url_acq_ctrl}"  # TODO: complete url
                
                try:
                    response = requests.post(url, files=file, timeout=10)
                    response.raise_for_status()
                except requests.exceptions.HTTPError as errh:
                    print("Http Error:", errh)
                    return False
                      
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex)
            return False
        
        return True

    def submit_status(self, record_id, percentage):  # pylint: disable=unused-argument
        """submit status to acq_control"""
        # TODO: Call endpoint on acq control
        return
    