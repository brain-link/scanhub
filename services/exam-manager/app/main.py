from fastapi import FastAPI
#from app.api.exam import exam
#from app.api.db import metadata, database, engine

#metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/exam/openapi.json", docs_url="/api/v1/exam/docs")

@app.on_event("startup")
async def startup():
    # await database.connect()
    pass

@app.on_event("shutdown")
async def shutdown():
    # await database.disconnect()
    pass

#app.include_router(exam, prefix='/api/v1/exam', tags=['exam'])