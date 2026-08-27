"""Helper methods for protocol, require recursive model translation."""

from scanhub_libraries.models import AcquisitionTaskOut, ProtocolOut, ResultOut

from app.db.postgres import Protocol, Task


async def get_protocol_out_model(data: Protocol) -> ProtocolOut:
    """Transform db model to pydantic model."""
    protocol = data.__dict__
    protocol["tasks"] = [await get_task_out(task) for task in data.tasks]
    return ProtocolOut(**protocol)


async def get_task_out(data: Task) -> AcquisitionTaskOut:
    """Transform db model to pydantic model."""
    task = data.__dict__
    task["results"] = [ResultOut(**result.__dict__) for result in data.results]
    return AcquisitionTaskOut(**task)
