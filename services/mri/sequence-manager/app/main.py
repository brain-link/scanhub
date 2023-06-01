import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from endpoints import mri_sequence_endpoints, health
from database.mongodb import connect_to_mongo, close_mongo_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate FastAPI app
app = FastAPI(
    openapi_url="/api/v1/mri/sequences/openapi.json",
    docs_url="/api/v1/mri/sequences/docs"
)


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Request: {request.method} {request.url}\n{str(exc)}")
    return JSONResponse(status_code=500, content={"detail": str(exc)})


# Include routers for endpoints
app.include_router(mri_sequence_endpoints.router, prefix="/api/v1/mri/sequences", tags=["MRI Sequences"])
app.include_router(health.router)


@app.on_event("startup")
async def startup_event():
    """
    Connect to MongoDB on startup.
    """
    logger.info("StartUp...")
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Close MongoDB connection on shutdown.
    """
    logger.info("ShutDown...")
    await close_mongo_connection()

# from fastapi import FastAPI
# from app.endpoints import health
# from app.database.mongodb import connect_to_mongo, close_mongo_connection
# import logging

# logger = logging.getLogger(__name__)

# logger.info("Instantiate APP...")

# app = FastAPI()

# @app.on_event("startup")
# async def startup_event():
#     logger.info("Connecting to MongoDB...")
#     await connect_to_mongo()

# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Disconnecting from MongoDB...")
#     await close_mongo_connection()

# logger.info("Adding API routers...")
# app.include_router(health.router)
