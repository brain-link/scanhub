"""Exam manager main file."""

from api.db import init_db, engine
from api.exam import router
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect


app = FastAPI(
    openapi_url="/api/v1/exam/openapi.json",
    docs_url="/api/v1/exam/docs",
)

# TODO: Specify specific origins
#   Wildcard ["*"] excludes eeverything that involves credentials
#   Better specify explicitly the allowed origins
#   See: https://fastapi.tiangolo.com/tutorial/cors/ 
origins = [
    "http://localhost",
    "http://localhost:3000",    # frontned
    "http://localhost:8100",    # patient-manager
    "http://localhost:8080",    # nginx
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=['*'],
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Statup exam-tree microservice.

    Raises
    ------
    HTTPException
        500: Device table does not exist
    HTTPException
        500: Workflow table does not exist
    """
    ins = inspect(engine)
    tables = ins.get_table_names()
    print(f"Existing tables: {tables}")
    if "device" not in tables:
        raise HTTPException(status_code=500, detail="SQL-DB: Device table is required but does not exist.")
    if "workflow" not in tables:
        raise HTTPException(status_code=500, detail="SQL-DB: Workflow table is required but does not exist.")
    init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown function."""
    return None


@router.get('/health/readiness', response_model={}, status_code=200, tags=['health'])
async def readiness() -> dict:
    """Readiness health endpoint.

    Returns
    -------
        Status dictionary

    Raises
    ------
    HTTPException
        500: Any of the exam-tree tables does not exist
    """
    ins = inspect(engine)
    exam_tables = ["exam", "procedure", "job", "record"]
    print(exam_tables)
    print(ins.get_table_names())
    # if not all(t in exam_tables for t in ins.get_table_names()):

    #     raise HTTPException(status_code=500, detail="SQL-DB: Could not create all required tables.")

    return {'status': 'ok'}


app.include_router(router, prefix='/api/v1/exam')
