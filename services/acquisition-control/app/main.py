"""Acquisition control. Receives control cmd from ui and controls scans on devices"""
#  python -m uvicorn acquisitioncontrol:app --reload
import logging
import uuid
import requests


from fastapi import FastAPI
from pydantic import BaseModel  # pylint: disable=no-name-in-module

DEVICE_URI = "host.docker.internal:8001"

# TODO: Move to scanhub-tools
class ScanJob(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanjob"""
    job_id: str

#TODO: Move to scanhub-tools
class ScanStatus(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of a scanjob"""
    record_id: str
    status_percent: int

#TODO: Move to scanhub-tools
class ScanRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """Pydantic definition of data to receive"""
    record_id: str

app = FastAPI(openapi_url="/api/v1/mri/acquisitioncontrol/openapi.json",
              docs_url="/api/v1/mri/acquisitioncontrol/docs")
logging.basicConfig(level=logging.DEBUG)


@app.post("/api/v1/mri/acquisitioncontrol/start-scan")
async def start_scan(scan_job: ScanJob):
    """Receives a job. Create a record id, trigger scan with it and returns it"""
    record_id = str(uuid.uuid4())
    logging.debug("Received job: %s, Generated record id: %s", scan_job.job_id, record_id)
    res = requests.post(f"http://{DEVICE_URI}/start-scan", json={"record_id": record_id}, timeout=60)
    print(res)
    return {"record_id": record_id}

@app.post("/api/v1/mri/acquisitioncontrol/forward-status")
async def forward_status(scan_status: ScanStatus):
    """Receives status for a job. Forwards it to the ui and returns ok."""
    return {"message": "Status submitted"}
