from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from scanhub.database.models import Patient
from server.scanhub.database.models import Device


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

@api_router.get("/")
async def read_root() -> dict:
    return dict(
        msg="Hello World!"
    )

@api_router.get("/patients/")
async def get_patients() -> dict:
    patients = await Patient.all()
    return patients

@api_router.get("/devices/")
async def get_devices() -> dict:
    devices = await Device.all()
    return devices

app.include_router(api_router)