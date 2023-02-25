from fastapi import FastAPI
from app.api.scancontrol import scancontrol

app = FastAPI(openapi_url="/api/v1/mri/scancontrol/openapi.json", docs_url="/api/v1/mri/scancontrol/docs")

@app.on_event("startup")
async def startup():
    # TBD
    pass

@app.on_event("shutdown")
async def shutdown():
    # TBD
    pass

app.include_router(scancontrol, prefix='/api/v1/mri/scancontrol', tags=['scancontrol'])