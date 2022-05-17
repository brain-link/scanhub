from scanhub.graphene.types import Patient, User, Device, Procedure, Recording, Site

from scanhub.database.models import Patient as PatientModel
from scanhub.database.models import Procedures as ProceduresModel
from scanhub.database.models import Recordings as RecordingsModel
from scanhub.database.models import Device as DeviceModel
from scanhub.database.models import Site as SiteModel
from scanhub.database.models import User as UserModel


class ModelUtilities:

    def __init__(self) -> None:
        pass

    async def create_device(self, id: int) -> Device:
        device = await DeviceModel.get(id=id)
        return Device(
            id=device.id,
            modality=device.modality,
            address=device.address,
            created_at=device.created_at,
            site=await self.create_site(device.site_id)
        )

    async def create_procedure(self, id: int) -> Procedure:
        procedure = await ProceduresModel.get(id=id)
        return Procedure(
            id=procedure.id,
            date=procedure.date,
            reason=procedure.reason,
            patient_id=procedure.patient_id
        )

    async def create_recording(self, id: int) -> Recording:
        recording = await RecordingsModel.get(id=id)
        return Recording(
            id=id,
            date=recording.date,
            comment=recording.comment,
            device=await self.create_device(recording.device_id),
            procedure=await self.create_procedure(recording.procedure_id)
        )

    async def create_patient(self, id: int) -> Patient:
        patient = await PatientModel.get(id=id)
        return Patient(
            id=id,
            sex=patient.sex,
            birthday=patient.birthday,
            concern=patient.concern,
            admission_date=patient.admission_date,
            status=patient.status
        )

    async def create_user(self, id: int) -> User:
        user = await UserModel.get(id=id)
        await user.fetch_related("patients")
        return User(
            id=id,
            name=user.username,
            patients=[await self.create_patient(patient.id) for patient in user.patients],
        )

    async def create_site(self, id: int) -> Site:
        site = await SiteModel.get(id=id)
        return Site(
            id=id,
            name=site.name,
            city=site.city,
            country=site.country,
            address=site.address
        ) 