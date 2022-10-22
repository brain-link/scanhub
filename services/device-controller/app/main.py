# Device Controller Service

from fastapi import FastAPI

description = """
Device Controller API

## Devices

User will be able to:

* **Register devices** (_not implemented_).
* **List devices** (_not implemented_).

## Controller

User can **operate devices**.
"""

app = FastAPI(
    openapi_url="/api/v1/device-controller/openapi.json", 
    docs_url="/api/v1/device-controller/docs"
    )

@app.get('/')
async def root():
    return {"message": "Device Controller Service"}