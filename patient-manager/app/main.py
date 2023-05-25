"""Patient manager main file."""

from app.api.connection_manager import ConnectionManager
from app.api.db import init_db
from app.api.routes import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ScanHub-UI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    """Initialize patient database. """
    init_db()


manager = ConnectionManager()

app.include_router(router)
