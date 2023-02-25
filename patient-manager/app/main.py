from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.routes import api_router
from app.connection_manager import ConnectionManager


# Define the app
app = FastAPI(
    title="ScanHub"
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

# Tortoise ORM    
register_tortoise(
    app,
    db_url='postgres://brainlink:data@patients_db/patients-data',
    modules={"models": [
        "app.models",
        ]},
    generate_schemas=True,
    add_exception_handlers=True,
)

manager = ConnectionManager()

# TODO: Put this to the api router?
@api_router.websocket("/ws/{client_id}")
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
