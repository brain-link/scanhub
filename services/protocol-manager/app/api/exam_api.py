# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Definition of protocol API endpoints."""

from typing import Annotated
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, HTTPException
from scanhub_libraries.models import BaseProtocol, ItemStatus, ProtocolOut, User
from scanhub_libraries.security import get_current_user, oauth2_scheme

from app import LOG_CALL_DELIMITER
from app.api import task_api
from app.dal import exam_dal as protocol_dal
from app.tools.helper import get_protocol_out_model

PREFIX_PATIENT_MANAGER = "http://patient-manager:8100/api/v1/patient"

exam_router = APIRouter(dependencies=[Depends(get_current_user)])


@exam_router.post("/new", response_model=ProtocolOut, status_code=201, tags=["protocols"], operation_id="create_protocol")
async def create_protocol(
    payload: BaseProtocol,
    user: Annotated[User, Depends(get_current_user)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ProtocolOut:
    """Create a new protocol."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Payload:", payload)
    if payload.status != "NEW":
        raise HTTPException(status_code=400, detail="New protocol needs to have status NEW.")
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given to create protocol.")
        with requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3,
        ) as getpatient_response:
            if getpatient_response.status_code != 200:
                raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Protocol template must not have patient_id.")
    if not (protocol := await protocol_dal.add_protocol_data(payload=payload, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create protocol")
    return await get_protocol_out_model(data=protocol)


@exam_router.post("/", response_model=ProtocolOut, status_code=201, tags=["protocols"], operation_id="create_protocol_from_template")
async def create_protocol_from_template(
    payload: BaseProtocol,
    template_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ProtocolOut:
    """Create a new protocol from template."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Protocol:", payload)
    print("template_id:", template_id)
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given to create protocol instance.")
        with requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3,
        ) as getpatient_response:
            if getpatient_response.status_code != 200:
                raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Protocol template must not have patient_id.")
    if not (template := await protocol_dal.get_protocol_data(protocol_id=template_id)):
        raise HTTPException(status_code=400, detail="Template not found.")
    if template.is_template is not True:
        raise HTTPException(
            status_code=400, detail="Request to create protocol from protocol instance instead of protocol template."
        )
    new_protocol = BaseProtocol(**payload.__dict__)
    new_protocol.status = ItemStatus.NEW
    if not (protocol := await protocol_dal.add_protocol_data(payload=new_protocol, creator=user.username)):
        raise HTTPException(status_code=404, detail="Could not create protocol.")

    protocol_out = await get_protocol_out_model(data=protocol)

    for task in template.tasks:
        protocol_out.tasks.append(
            await task_api.create_task_from_template(
                protocol_id=protocol.id,
                template_id=task.id,
                new_task_is_template=protocol.is_template,
                user=user,
            )
        )
    return protocol_out


@exam_router.get("/{exam_id}", response_model=ProtocolOut, status_code=200, tags=["protocols"], operation_id="get_protocol")
async def get_protocol(exam_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> ProtocolOut:
    """Get protocol endpoint."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    try:
        _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Badly formed exam_id")
    if not (protocol := await protocol_dal.get_protocol_data(protocol_id=_id)):
        raise HTTPException(status_code=404, detail="Protocol not found")
    return await get_protocol_out_model(data=protocol)


@exam_router.get("/all/{patient_id}", response_model=list[ProtocolOut], status_code=200, tags=["protocols"], operation_id="get_all_patient_protocols")
async def get_all_patient_protocols(
    patient_id: UUID, user: Annotated[User, Depends(get_current_user)]
) -> list[ProtocolOut]:
    """Get all protocols of a certain patient."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Getting protocols for patient_id:", patient_id)
    if not (protocols := await protocol_dal.get_all_protocol_data(patient_id=patient_id)):
        return []
    return [await get_protocol_out_model(data=p) for p in protocols]


@exam_router.get("/templates/all", response_model=list[ProtocolOut], status_code=200, tags=["protocols"], operation_id="get_all_protocol_templates")
async def get_all_protocol_templates(user: Annotated[User, Depends(get_current_user)]) -> list[ProtocolOut]:
    """Get all protocol templates."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    if not (protocols := await protocol_dal.get_all_protocol_template_data()):
        return []
    result = [await get_protocol_out_model(data=p) for p in protocols]
    print("Number of protocol templates: ", len(result))
    return result


@exam_router.delete("/{exam_id}", response_model={}, status_code=204, tags=["protocols"], operation_id="delete_protocol")
async def protocol_delete(exam_id: UUID | str, user: Annotated[User, Depends(get_current_user)]) -> None:
    """Delete a protocol by id. Cascade deletes the associated tasks."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not await protocol_dal.delete_protocol_data(protocol_id=_id):
        raise HTTPException(status_code=404, detail="Could not delete protocol.")


@exam_router.put("/{exam_id}", response_model=ProtocolOut, status_code=200, tags=["protocols"], operation_id="update_protocol")
async def update_protocol(
    exam_id: UUID | str,
    payload: BaseProtocol,
    user: Annotated[User, Depends(get_current_user)],
    access_token: Annotated[str, Depends(oauth2_scheme)],
) -> ProtocolOut:
    """Update an existing protocol."""
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("exam_id:", exam_id)
    if payload.is_template is False:
        if payload.patient_id is None:
            raise HTTPException(status_code=400, detail="patient_id must be given for protocol instance.")
        with requests.get(
            PREFIX_PATIENT_MANAGER + "/" + str(payload.patient_id),
            headers={"Authorization": "Bearer " + access_token},
            timeout=3,
        ) as getpatient_response:
            if getpatient_response.status_code != 200:
                raise HTTPException(status_code=400, detail="patient_id must refer to an existing patient.")
    if payload.is_template is True and payload.patient_id is not None:
        raise HTTPException(status_code=400, detail="Protocol template must not have patient_id.")
    if payload.status == "NEW":
        raise HTTPException(status_code=403, detail="Protocol cannot be updated to status NEW.")
    _id = UUID(exam_id) if not isinstance(exam_id, UUID) else exam_id
    if not (protocol_updated := await protocol_dal.update_protocol_data(protocol_id=_id, payload=payload)):
        raise HTTPException(status_code=404, detail="Could not update protocol.")
    return await get_protocol_out_model(data=protocol_updated)
