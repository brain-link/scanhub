from fastapi import FastAPI
from fastapi.routing import APIRoute
from api.exam import exam

# from api.db import Exam, Procedure, Record
# from sqlalchemy import inspect


def custom_client_uid(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"

app = FastAPI(
    openapi_url="/api/v1/exam/openapi.json", 
    docs_url="/api/v1/exam/docs",
    generate_unique_id_function=custom_client_uid,
)

@app.on_event("startup")
async def startup():
    pass
    # map_exam, map_procedure, map_record = inspect(Exam), inspect(Procedure), inspect(Record)
    # print(f"***** INSPECT *****\n")
    # print(f"Columns:\n{map_exam.columns}\n{map_procedure.columns}\n{map_record.columns}")
    # print(f"Relationships:\n{map_exam.relationships}\n{map_procedure.relationships}\n{map_record.relationships}")

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(exam, prefix='/api/v1/exam', tags=['exam'])