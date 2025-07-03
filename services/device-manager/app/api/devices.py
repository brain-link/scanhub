# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""
Device API Endpoints.

This module defines the API routes and WebSocket endpoints for managing devices.
It includes functionalities for:
- CRUD operations on devices.
- Device registration and status updates via WebSocket.

Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""
# pylint: disable=no-name-in-module
# pylint: disable=too-many-statements

import json
from secrets import compare_digest, token_hex
from typing import Annotated, Dict, List
from uuid import UUID

import requests
from fastapi import APIRouter, Depends, Header, HTTPException, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    AcquisitionTaskOut,
    MRISequenceOut,
    DeviceCreationRequest,
    DeviceDetails,
    DeviceOut,
    ItemStatus,
    TaskOut,
    User,
)
from scanhub_libraries.security import compute_complex_password_hash, get_current_user
from sqlalchemy import exc

from api.dal import (
    dal_create_device,
    dal_delete_device,
    dal_get_all_devices,
    dal_get_device,
    dal_update_device,
)
from api.db import Device

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

EXAM_MANAGER_URI = "exam-manager:8000"
LOG_CALL_DELIMITER = "-------------------------------------------------------------------------------"


# The dependency on get_current_user that is declared here does not inherit
# to websockets but only to regular http endpoints.
router = APIRouter(dependencies=[Depends(get_current_user)])

# Maintain active WebSocket connections and a mapping of device IDs to WebSockets
dict_id_websocket: Dict[UUID, WebSocket] = {}


async def get_device_out(data: Device) -> DeviceOut:
    """Get pydantic device output model helper function.

    Parameters
    ----------
    data
        Database model

    Returns
    -------
        Pydantic output model
    """
    return DeviceOut(
        id=data.id,
        datetime_created=data.datetime_created,
        datetime_updated=data.datetime_updated,
        name=data.name,
        manufacturer=data.manufacturer,
        modality=data.modality,
        status=data.status,
        site=data.site,
        ip_address=data.ip_address,
        title=data.title,
        description=data.description
    )



@router.get('/', response_model=List[DeviceOut], status_code=200, tags=["devices"])
async def get_devices(current_user: Annotated[User, Depends(get_current_user)]) -> list[DeviceOut]:
    """
    Retrieve the list of registered devices.

    Returns
    -------
        List[Device]: The list of registered devices.
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", current_user.username)
    if not (devices_all := await dal_get_all_devices()):
        # Don't raise exception here, list might be empty
        return []
    return [await get_device_out(device) for device in devices_all]


@router.get('/{device_id}', response_model=DeviceOut, status_code=200, tags=["devices"])
async def get_device(current_user: Annotated[User, Depends(get_current_user)], device_id: UUID):
    """
    Retrieve a specific device.

    Args
    -------
        device_id (str): The ID of the device.

    Returns
    -------
        dict: The response containing the information about the device
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", current_user.username)
    print("Device-ID:", device_id)
    if not (device := await dal_get_device(device_id)):
        raise HTTPException(status_code=404, detail="Device not found")
    return await get_device_out(device)


@router.post("/createdevice", status_code=201, tags=["devices"])
async def create_device(current_user: Annotated[User, Depends(get_current_user)], request: DeviceCreationRequest):
    """
    Create device database entry.

    Only devices which are created by a user via this endpoint and have the device_id and device_token
    that result from this call configured correctly can later connect and register.

    Parameters
    ----------
    request:
        DeviceCreationRequest to create device in Scanhub.
        Further details of the device are later provided by the device itself.

    Return
    ------
    device_token:
        the token of the device which the user should copy manually to the configuration file of the device.

    device_id:
        the id of the device, should be copied to the devices config file together with the device_token.
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", current_user.username)
    print("Request:", request)

    if len(request.title) < 1:
        raise HTTPException(
            status_code=400,
            detail="The title must not be empty!")
    if len(request.description) < 1:
        raise HTTPException(
            status_code=400,
            detail="The description name must not be empty!")

    device_token = token_hex(1024)  # create new token
    salt = token_hex(1024)  # create new salt
    hashed_token = compute_complex_password_hash(device_token, salt)
    device = await dal_create_device(request, hashed_token, salt)

    return {"device_token": device_token, "device_id": device.id}


@router.delete('/{device_id}', response_model={}, status_code=204, tags=["devices"])
async def delete_device(device_id: UUID):
    """
    Delete a device.

    Args
    -------
        device_id (str): The ID of the device.

    Returns
    -------
        dict: The response indicating the success or failure of the deletion.
    """
    if not await dal_delete_device(device_id):
        raise HTTPException(status_code=404, detail="Device not found")


@router.post('/start_scan_via_websocket', response_model={}, status_code=200, tags=["devices"])
async def start_scan_via_websocket(
    task: AcquisitionTaskOut,
    access_token: Annotated[str, Depends(oauth2_scheme)]
):
    """Start a scan via a websocket that was already opened by the device.

    Parameters
    ----------
    device_task
        Details of the scan and the device to scan on.

    """
    headers = {"Authorization": "Bearer " + access_token}
    print("Start scan via websocket with task:", task)

    # Get pulseq sequence
    get_seq_response = requests.get(
        f"http://{EXAM_MANAGER_URI}/api/v1/exam/sequence/{task.sequence_id}", headers=headers, timeout=3
    )
    if not get_seq_response.status_code == 200:
        raise HTTPException(status_code=404, detail="Sequence not found")

    payload = {
        "trace_id": task.id,
        "mrd_header": "",
        "sequence": MRISequenceOut(**get_seq_response.json()),
        "acquisition_parameter": task.acquisition_parameter,
        "acquisition_limits": task.acquisition_limits,
    }

    print("Device payload: ", payload)
    return
        
    # if task.device_id in dict_id_websocket:
    #     websocket = dict_id_websocket[task.device_id]
    #     await websocket.send_text(
    #         json.dumps(
    #             {'command': 'start', 'data': task},
    #             default=jsonable_encoder
    #         ))
    #     return
    # else:
    #     raise HTTPException(status_code=503, detail='Device offline.')


async def connection_with_valid_id_and_token(device_id: Annotated[UUID, Header()],
                                             device_token: Annotated[str, Header()]):
    """
    Check if the given device_id and device_token belong to an existing device in the database.

    Args
    ----
        device_id (UUID): The device_id to check against the database.
        device_token (str): The device_token to check against the database.
    """
    if not (device := await dal_get_device(device_id)):
        # do the same steps as if user existed to avoid disclosing info about existence of users
        dummy_hash = compute_complex_password_hash(device_token, token_hex(1024))
        compare_digest(dummy_hash, dummy_hash)
        print('Invalid device_id:', device_id)
        raise WebSocketException(code=1008, reason='Invalid device_id or device_token')
    # check token for user
    received_token_hash = compute_complex_password_hash(device_token, device.salt)
    token_match = compare_digest(received_token_hash, device.token_hash)
    if not token_match:
        print('Invalid device_token', device_token, 'for device_id', device_id)
        raise WebSocketException(code=1008, reason='Invalid device_id or device_token')
    return device_id


# The dependency on get_current_user that is declared at the creation of the router does not inherit to this websocket
# but only to regular http endpoints.
# pylint: disable=locally-disabled, too-many-branches
# TODO improve overall logic and resilience
@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket,
                             device_id: Annotated[UUID, Depends(connection_with_valid_id_and_token)]):
    """
    Websocket endpoint for device communication.

    Args
    ----
        websocket (WebSocket): The WebSocket connection object.
        device_id (UUID): The device_id.
    """
    await websocket.accept()
    print('Device connected on websocket.')
    try:
        dict_id_websocket[device_id] = websocket
        while True:
            message = await websocket.receive_json()
            print("Received messgage:", message)
            command = message.get('command')
            # ===============  Register device ===================
            if command == 'register':
                print("Handle command 'register'.")
                try:
                    device_details = message.get('data')
                    device_details_object = DeviceDetails(**device_details)
                    await dal_update_device(device_id, device_details_object.dict())
                    print('Device registered.')
                    # Send response to the device
                    await websocket.send_json({
                        'command': 'feedback',
                        'message': 'Device registered successfully'})
                except exc.SQLAlchemyError as exception:
                    print('Error registering device: ', exception)
                    await websocket.send_json({'message': 'Error registering device' + str(exception)})

            # ================ Update device status ===============
            elif command == 'update_status':
                print("Handle command 'update_status'.")
                status = str(message.get('status'))
                data = message.get('data')

                if not await dal_update_device(device_id, {"status": status}):
                    print('Error updating device, device_id:', device_id)
                    await websocket.send_json({'message': 'Error updating device.'})
                print("Device status updated.")

                if status == 'SCANNING':
                    record_id = str(message.get('record_id'))
                    user_access_token = str(message.get('user_access_token'))
                    headers = {"Authorization": "Bearer " + user_access_token}
                    get_task_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{record_id}",
                                                     headers=headers,
                                                     timeout=3)
                    print("Get task, status_code:", get_task_response.status_code)
                    if get_task_response.status_code != 200:
                        await websocket.send_json({'message': 'Invalild record id for update_status scanning.'})
                        continue
                    task_raw = get_task_response.json()
                    task = TaskOut(**task_raw)
                    if data['progress'] == 100:
                        print("Scanning progress 100% --> set task status to finished")
                        task.status = ItemStatus.FINISHED
                    task.progress = data['progress']
                    put_task_response = requests.put(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{record_id}",
                                                     data=json.dumps(task, default=jsonable_encoder),
                                                     headers=headers,
                                                     timeout=3)
                    if put_task_response.status_code != 200:
                        await websocket.send_json({'message': 'Error at updating task status in DB.'})

                    print("Task progress updated.")

                await websocket.send_json({
                    'command': 'feedback',
                    'message': 'Device status updated successfully'})
            else:
                print("Received unknown command, which will be ignored:", command)

    except WebSocketDisconnect:
        print("WebSocketDisconnect")
        del dict_id_websocket[device_id]
        print('Device disconnected:', device_id)
        # Set the status of the disconnected device to "disconnected"
        if not await dal_update_device(device_id, {"status": "DISCONNECTED"}):
            print('Error updating device status to disconnected.')
