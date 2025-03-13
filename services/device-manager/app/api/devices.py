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
from datetime import datetime
from typing import Dict, List

import requests
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from scanhub_libraries.models import DeviceTask, ItemStatus, TaskOut
from scanhub_libraries.security import get_current_user
from sqlalchemy import exc

from .dal import (
    dal_create_device,
    dal_delete_device,
    dal_get_all_devices,
    dal_get_device,
    dal_update_device,
)
from .models import BaseDevice, DeviceOut, get_device_out

router = APIRouter(dependencies=[Depends(get_current_user)])


EXAM_MANAGER_URI = "exam-manager:8000"


# Maintain active WebSocket connections and a mapping of device IDs to WebSockets
active_connections: list[WebSocket] = []
dict_id_websocket: Dict[str, WebSocket] = {}


@router.get('/', response_model=List[DeviceOut], status_code=200, tags=["devices"])
async def get_devices() -> list[DeviceOut]:
    """
    Retrieve the list of registered devices.

    Returns
    -------
        List[Device]: The list of registered devices.
    """
    if not (devices_all := await dal_get_all_devices()):
        # Don't raise exception here, list might be empty
        return []
    return [await get_device_out(device) for device in devices_all]


@router.get('/{device_id}/ip_address', tags=["devices"])
async def get_device_ip_address(device_id: str):
    """
    Retrieve the IP address of a specific device.

    Args
    -------
        device_id (str): The ID of the device.

    Returns
    -------
        dict: The response containing the IP address of the device.
    """
    if not (device := await dal_get_device(device_id)):
        raise HTTPException(status_code=404, detail="Device not found")
    return {'ip_address': device.ip_address}


@router.get('/{device_id}', response_model=DeviceOut, status_code=200, tags=["devices"])
async def get_device(device_id: str):
    """
    Retrieve a specific device.

    Args
    -------
        device_id (str): The ID of the device.

    Returns
    -------
        dict: The response containing the information about the device
    """
    if not (device := await dal_get_device(device_id)):
        raise HTTPException(status_code=404, detail="Device not found")
    return await get_device_out(device)


@router.get('/{device_id}/status', tags=["devices"])
async def get_device_status(device_id: str):
    """
    Retrieve the status of a specific device.

    Args
    -------
        device_id (str): The ID of the device.

    Returns
    -------
        dict: The response containing the status of the device.
    """
    if not (device := await dal_get_device(device_id)):
        raise HTTPException(status_code=404, detail="Device not found")

    status = device.status
    # Return the current status of the device
    return {'status': status}


@router.delete('/{device_id}', response_model={}, status_code=204, tags=["devices"])
async def delete_device(device_id: str):
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
async def start_scan_via_websocket(device_task: DeviceTask):
    """Start a scan via a websocket that was already opened by the device.

    Parameters
    ----------
    device_task
        Details of the scan and the device to scan on.

    """
    print("start_scan_via_websocket")
    print("device_task:", device_task)
    if device_task.device_id in dict_id_websocket:
        websocket = dict_id_websocket[device_task.device_id]
        await websocket.send_text(json.dumps({'command': 'start', 'data': device_task}, default=jsonable_encoder))
        return
    else:
        raise HTTPException(status_code=503, detail='Device offline.')


# TODO restrict access to token-bearer
# (currently it is not restricted because the current dependency on get_current_user in the APIRouter
# is only applicable to regular HTTP Connections)
# https://fastapi.tiangolo.com/advanced/websockets/#using-depends-and-others
# https://fastapi.tiangolo.com/reference/websockets/ (see first tip)
# https://github.com/DontPanicO/fastapi-distributed-websocket/blob/main/distributed_websocket/_auth.py
# https://github.com/fastapi/fastapi/blob/5614b94ccc9f72f1de2f63aae63f5fe90b86c8b5/fastapi/security/oauth2.py#L139
# https://fastapi.tiangolo.com/reference/exceptions/
# pylint: disable=locally-disabled, too-many-branches
@router.websocket('/ws2')
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket endpoint for device communication.

    Args
    ----
        websocket (WebSocket): The WebSocket connection object.
    """
    await websocket.accept()
    active_connections.append(websocket)

    print('Device connected on ws2.')

    device_id_global = ""

    try:
        while True:
            message = await websocket.receive_json()
            print("Received messgage:", message)
            command = message.get('command')
            # ===============  Register device ===================
            if command == 'register':
                print("Received command 'register'.")
                if device_id_global != "":
                    await websocket.send_json({'message': 'Error registering device. \
In this session a device already was registered.'})
                    continue
                device_data = message.get('data')
                device_id = device_data.get('id')
                device = BaseDevice(**device_data)

                if not (await dal_get_device(device_id)):
                    try:
                        await dal_create_device(device)
                    except exc.SQLAlchemyError as ex:
                        print('Error registering device: ', device, ex)
                        await websocket.send_json({'message': 'Error registering device' + str(ex)})
                        continue
                    print('Device registered:', device)
                    # Send response to the device
                    await websocket.send_json({
                        'command': 'feedback',
                        'message': 'Device registered successfully'})
                else:
                    await websocket.send_json({
                        'command': 'feedback',
                        'message': 'Device already registered'})

                device_id_global = device_id
                dict_id_websocket[device_id] = websocket

            # ================ Update device status ===============
            elif command == 'update_status':
                print("Received command 'update_status'.")
                status = str(message.get('status'))
                data = message.get('data')
                device_id = message.get('device_id')
                if device_id_global not in ("", device_id):
                    await websocket.send_json({'message': 'Error updating device. \
Device ID does not match'})
                    continue
                if not (device_to_update := await dal_get_device(device_id)):
                    await websocket.send_json({'message': 'Device not registered'})
                    continue

                device_out = await get_device_out(device_to_update)
                # Update the device's status and last_status_update
                device_out.status = status
                device_out.datetime_updated = datetime.now()

                if not await dal_update_device(device_id, device_out):
                    await websocket.send_json({'message': 'Error updating device.'})

                if status == 'scanning':
                    print("Scanning progress 100% --> set task status to finished")
                    record_id = str(message.get('record_id'))
                    user_access_token = str(message.get('user_access_token'))
                    headers = {"Authorization": "Bearer " + user_access_token}
                    get_task_response = requests.get(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{record_id}",
                                                     headers=headers)
                    print("Get task, status_code:", get_task_response.status_code)
                    if get_task_response.status_code != 200:
                        await websocket.send_json({'message': 'Invalild record id for update_status scanning.'})
                        continue
                    task_raw = get_task_response.json()
                    task = TaskOut(**task_raw)
                    if data['progress'] == 100:
                        task.status = ItemStatus.FINISHED
                    task.progress = data['progress']
                    put_task_response = requests.put(f"http://{EXAM_MANAGER_URI}/api/v1/exam/task/{record_id}",
                                                     data=json.dumps(task, default=jsonable_encoder),
                                                     headers=headers)
                    if put_task_response.status_code != 200:
                        await websocket.send_json({'message': 'Error at updating task status in DB.'})

                await websocket.send_json({
                    'command': 'feedback',
                    'message': 'Device status updated successfully'})
                # device_id_global = device_id    # (not needed?)
                # dict_id_websocket[device_id] = websocket   # (not needed?)
            else:
                print("Received unknown command, which will be ignored:", command)


    except WebSocketDisconnect:
        print("WebSocketDisconnect")
        active_connections.remove(websocket)
        if device_id_global in dict_id_websocket:
            del dict_id_websocket[device_id_global]
        print('Device disconnected:', device_id_global)
        # Set the status of the disconnected device to "disconnected"
        if not (device_to_update := await dal_get_device(device_id_global)):
            print('Device not registered')
        else:
            device_out = await get_device_out(device_to_update)
            # Update the device's status and last_status_update
            device_out.status = 'disconnected'
            device_out.datetime_updated = datetime.now()
            if not await dal_update_device(device_id, device_out):
                print('Error updating device.')
            else:
                # Send response to the device
                print('Device status updated successfully')


# TODO restrict access to token-bearer
# (currently it is not restricted because the current dependency on get_current_user in the APIRouter
# is only applicable to regular HTTP Connections)
# https://fastapi.tiangolo.com/advanced/websockets/#using-depends-and-others
# https://fastapi.tiangolo.com/reference/websockets/ (see first tip)
# https://github.com/DontPanicO/fastapi-distributed-websocket/blob/main/distributed_websocket/_auth.py
# https://github.com/fastapi/fastapi/blob/5614b94ccc9f72f1de2f63aae63f5fe90b86c8b5/fastapi/security/oauth2.py#L139
# https://fastapi.tiangolo.com/reference/exceptions/
@router.websocket('/ws')
async def websocket_endpoint_legacy(websocket: WebSocket):
    """
    Websocket endpoint for device communication (legacy). Used for old way over acquisition-manager.

    Args
    ----
        websocket (WebSocket): The WebSocket connection object.
    """
    await websocket.accept()
    active_connections.append(websocket)

    print('Device connected on ws.')

    device_id_global = ""

    try:
        while True:
            message = await websocket.receive_json()
            print("Received messgage:", message)
            command = message.get('command')
            # ===============  Register device ===================
            if command == 'register':
                if device_id_global != "":
                    await websocket.send_json({'message': 'Error registering device. \
In this session a device already was registered.'})
                    continue
                device_data = message.get('data')
                ip_address = message.get('ip_address')
                device_id = device_data.get('id')
                device = BaseDevice(ip_address=ip_address, **device_data)
                try:
                    await dal_create_device(device)
                except exc.SQLAlchemyError as ex:
                    print('Error registering device: ', device, ex)
                    await websocket.send_json({'message': 'Error registering device' + str(ex)})
                    continue
                print('Device registered:', device)
                # Send response to the device
                await websocket.send_json({'message': 'Device registered successfully'})
                device_id_global = device_id
                dict_id_websocket[device_id] = websocket

            # ================ Update device status ===============
            elif command == 'update_status':
                status_data = message.get('data')
                device_id = status_data.get('id')
                if device_id_global not in ("", device_id):
                    await websocket.send_json({'message': 'Error updating device. \
Device ID does not match'})
                elif not (device_to_update := await dal_get_device(device_id)):
                    await websocket.send_json({'message': 'Device not registered'})
                else:
                    device_out = await get_device_out(device_to_update)
                    # Update the device's status and last_status_update
                    device_out.status = status_data.get('status')
                    device_out.datetime_updated = datetime.now()
                    if not await dal_update_device(device_id, device_out):
                        await websocket.send_json({'message': 'Error updating device.'})
                    else:
                        # Send response to the device
                        await websocket.send_json({'message': 'Device status updated successfully'})
                        device_id_global = device_id
                        dict_id_websocket[device_id] = websocket

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        if device_id_global in dict_id_websocket:
            del dict_id_websocket[device_id_global]
        print('Device disconnected:', device_id_global)
        # Set the status of the disconnected device to "disconnected"
        if not (device_to_update := await dal_get_device(device_id_global)):
            print('Device not registered')
        else:
            device_out = await get_device_out(device_to_update)
            # Update the device's status and last_status_update
            device_out.status = 'disconnected'
            device_out.datetime_updated = datetime.now()
            if not await dal_update_device(device_id, device_out):
                print('Error updating device.')
            else:
                # Send response to the device
                print('Device status updated successfully')

