# import uvicorn
from fastapi import FastAPI, APIRouter, Request, Path, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from tortoise.contrib.fastapi import register_tortoise
from scanhub.database.models import Patient
from scanhub.database.models import Device



class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            
manager = ConnectionManager()

app = FastAPI(
    title="ScanHub"
)

api_router = APIRouter()

# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

# Tortoise ORM    
register_tortoise(
    app,
    db_url='postgres://brainLink:brainLinkIstCool2022UndLecker@postgres/scanhub',
    modules={"models": ["scanhub.database.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

# TODO: Do the routing in a different routes.py file
@app.get("/")
async def root() -> dict:
    return dict(
        msg="Hello World!"
    )

@api_router.get("/patients/")
async def get_patients() -> dict:
    patients = await Patient.all()
    return patients
    # return [dict(
    #     id=patient.id,
    #     sex=patient.sex,
    #     birthday=patient.birthday,
    #     concern=patient.concern,
    #     status=patient.status
    # ) for patient in patients]

@api_router.get("/devices/")
async def get_devices() -> dict:
    devices = await Device.all()
    return devices


@api_router.get("/patients/{patient_id}/")
async def get_patient(patient_id: int) -> dict:
    patient = await Patient.get(id=patient_id)
    return patient


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

app.include_router(api_router)

# if __name__ == "__main__":
#     uvicorn.run("api:app", host="0.0.0.0", reload=True, port=8000)
