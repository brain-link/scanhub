# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Patient manager main file."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scanhub_libraries.security import get_current_user

from api.db import init_db
from api.routes import router

app = FastAPI(
    openapi_url="/api/v1/patient/openapi.json",
    docs_url="/api/v1/patient/docs",
    title="ScanHub-UI",
    dependencies=[Depends(get_current_user)]
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


app.include_router(router, prefix="/api/v1/patient")
