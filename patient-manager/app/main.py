"""Patient manager main file."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.db import init_db
from .api.routes import router

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
    """Initialize patient database."""
    init_db()


app.include_router(router)
