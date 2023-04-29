from fastapi import FastAPI #, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
# from tortoise.contrib.fastapi import register_tortoise

from api.routes import patient
from api.connection_manager import ConnectionManager
from api.db import init_db


app = FastAPI(
    title="ScanHubUi"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    init_db()

@app.on_event("shutdown")
async def shutdown():
    pass

# # Tortoise ORM    
# register_tortoise(
#     app,
#     db_url='postgres://brainlink:data@patients_db/patients-data',
#     modules={"models": [
#         "app.models",
#         ]},
#     generate_schemas=True,
#     add_exception_handlers=True,
# )

manager = ConnectionManager()

app.include_router(patient)


# TODO: Put this to the api router?
# @api_router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")