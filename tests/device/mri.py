from fastapi import FastAPI
from pydantic import BaseModel

RECORDS_PATH = "./records/"

class ScanRequest(BaseModel):
    record_id: str

app = FastAPI()



@app.post("/start-scan")
async def root(scanRequest: ScanRequest):
    sequence = open(f"{RECORDS_PATH}{scanRequest.record_id}/sequence", "r")
    print(sequence.read())
    return 


def start_scan():
    pass
