# from fastapi import FastAPI
# from app.api.devices import devices
# from app.api.db import metadata, database, engine

# metadata.create_all(engine)

# app = FastAPI(openapi_url="/api/v1/devices/openapi.json", docs_url="/api/v1/devices/docs")

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()



import logging
from enum import Enum
from typing import Any, List

from fastapi import APIRouter, Body, FastAPI, HTTPException, status
from pydantic import BaseModel
from starlette.endpoints import WebSocketEndpoint
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.websockets import WebSocket

from pool import DeviceInfo, Pool

from api.db import init_db


# app = FastAPI()  # pylint: disable=invalid-name
app = FastAPI(
    openapi_url="/api/v1/device/openapi.json",
    docs_url="/api/v1/device/docs"
)
# router = APIRouter()
# app.include_router(router, prefix='/api/v1/devices')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.debug = True

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PoolEventMiddleware:  # pylint: disable=too-few-public-methods
    """Middleware for providing a global :class:`~.Pool` instance to both HTTP
    and WebSocket scopes.

    Although it might seem odd to load the broadcast interface like this (as
    opposed to, e.g. providing a global) this both mimics the pattern
    established by starlette's existing DatabaseMiddlware, and describes a
    pattern for installing an arbitrary broadcast backend (Redis PUB-SUB,
    Postgres LISTEN/NOTIFY, etc) and providing it at the level of an individual
    request.
    """

    def __init__(self, app: ASGIApp):
        self._app = app
        self._pool = Pool()

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] in ("lifespan", "http", "websocket"):
            scope["pool"] = self._pool
        await self._app(scope, receive, send)



app.add_middleware(PoolEventMiddleware)


@app.get("/")
def home():
    """Serve static index page.
    """
    return FileResponse("static/index.html")

@app.on_event("startup")
async def startup():
    # await create_db()
    init_db()

# @app.get('/healthcheck', status_code=status.HTTP_200_OK)
# def perform_healthcheck():
#     return {'healthcheck': 'healthy'}


class DeviceListResponse(BaseModel):
    """Response model for /list_devices endpoint.
    """

    devices: List[str]


@app.get("/devices", response_model=DeviceListResponse)
async def list_devices(request: Request):
    """List all devices connected to the pool.
    """
    pool: Pool | None = request.get("pool")
    if pool is None:
        raise HTTPException(500, detail="Global `Pool` instance unavailable!")
    return {"devices": pool.device_list}


class DeviceInfoResponse(DeviceInfo):
    """Response model for /devices/:device_id endpoint.
    """

@app.get("/devices/{device_id}", response_model=DeviceInfoResponse)
async def get_device_info(request: Request, device_id: str):
    pool: Pool | None = request.get("pool")
    if pool is None:
        raise HTTPException(500, detail="Global `Pool` instance unavailable!")
    device = pool.get_device(device_id)
    if device is None:
        raise HTTPException(404, detail=f"No such device: {device_id}")
    return device


@app.post("/devices/{device_id}/remove", response_model=DeviceListResponse)
async def remove_device(request: Request, device_id: str):
    """List all devices connected to the pool.
    """
    pool: Pool | None = request.get("pool")
    if pool is None:
        raise HTTPException(500, detail="Global `Pool` instance unavailable!")
    try:
        await pool.remove_device(device_id)
    except ValueError:
        raise HTTPException(404, detail=f"No such device: {device_id}")


@app.post("/send/{device_id}/{message}")
async def send_to_device(request: Request, device_id: str, message: str):
    """List all devices connected to the pool.
    """
    pool: Pool | None = request.get("pool")
    if pool is None:
        raise HTTPException(500, detail="Global `Pool` instance unavailable!")
    try:
        await pool.send_to_device(device_id, message)
    except ValueError:
        raise HTTPException(404, detail=f"No such device: {device_id}")


class Distance(str, Enum):
    """Distance classes for the /thunder endpoint.
    """

    Near = "near"
    Far = "far"
    Extreme = "extreme"


class ThunderDistance(BaseModel):
    """Indicator of distance for /thunder endpoint.
    """

    category: Distance

@app.post("/thunder")
async def thunder(request: Request, distance: ThunderDistance = Body(...)):
    """Broadcast an ambient message to all chat pool devices.
    """
    pool: Pool | None = request.get("pool")
    if pool is None:
        raise HTTPException(500, detail="Global `Pool` instance unavailable!")
    if distance.category == Distance.Near:
        await pool.broadcast_message("server", "Thunder booms overhead")
    elif distance.category == Distance.Far:
        await pool.broadcast_message("server", "Thunder rumbles in the distance")
    else:
        await pool.broadcast_message("server", "You feel a faint tremor")


@app.websocket_route("/api/v1/devices/ws", name="ws")
class PoolLive(WebSocketEndpoint):
    """Live connection to the global :class:`~.Pool` instance, via WebSocket.
    """
    encoding: str = "text"
    session_name: str = ""
    count: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pool: Pool | None = None
        self.device_id: str | None = None

    @classmethod
    def get_next_device_id(cls):
        """Returns monotonically increasing numbered devicenames in the form
            'device_[number]'
        """
        device_id: str = f"device_{cls.count}"
        cls.count += 1
        return device_id

    async def on_connect(self, websocket):
        """Handle a new connection.

        New devices are assigned a device ID and notified of the pool's connected
        devices. The other connected devices are notified of the new device's arrival,
        and finally the new device is added to the global :class:`~.Pool` instance.
        """
        log.info("Connecting new device...")
        pool: Pool | None = self.scope.get("pool")
        if pool is None:
            raise RuntimeError(f"Global `Pool` instance unavailable!")
        self.pool = pool
        self.device_id = self.get_next_device_id()
        await websocket.accept()
        await websocket.send_json(
            {"type": "POOL_JOIN", "data": {"device_id": self.device_id}}
        )
        await self.pool.broadcast_device_joined(self.device_id)
        self.pool.add_device(self.device_id, websocket)

    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        """Disconnect the device, removing them from the :class:`~.Pool`, and
        notifying the other devices of their departure.
        """
        if self.device_id is None:
            raise RuntimeError(
                "PoolLive.on_disconnect() called without a valid device_id"
            )
        self.pool.remove_device(self.device_id)
        await self.pool.broadcast_device_left(self.device_id)

    async def on_receive(self, _websocket: WebSocket, msg: Any):
        """Handle incoming message: `msg` is forwarded straight to `broadcast_message`.
        """
        if self.device_id is None:
            raise RuntimeError("PoolLive.on_receive() called without a valid device_id")
        if not isinstance(msg, str):
            raise ValueError(f"PoolLive.on_receive() passed unhandleable data: {msg}")
        await self.pool.broadcast_message(self.device_id, msg)



