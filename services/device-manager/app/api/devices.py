"""
Device API Endpoints.

This module defines the API routes and WebSocket endpoints for managing devices.
It includes functionalities for:
- CRUD operations on devices.
- Device registration and status updates via WebSocket.
- Health readiness checks.

Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""

# pylint: disable=no-name-in-module
# pylint: disable=too-many-statements

from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import exc

from .dal import (
    dal_create_device,
    dal_delete_device,
    dal_get_all_devices,
    dal_get_device,
    dal_update_device,
)
from .models import DeviceOut, get_device_out

router = APIRouter()

# Maintain active WebSocket connections and a mapping of device IDs to WebSockets
active_connections: list[WebSocket] = []
dict_id_websocket: Dict[str, WebSocket] = {}

@router.get("/health/readiness", response_model={}, status_code=200, tags=["health"])
async def readiness() -> dict:
    """
    Readiness health endpoint.

    Checks if the service is ready to handle requests.

    Returns
    -------
    dict
        A dictionary with the readiness status.
    """
    return {"status": "ok"}


@router.put('/{device_id}/start-scan', status_code=200, tags=["devices"])
async def start_scan(device_id: str, header_xml: str, sequence_data: str, acquisition_data: str):
    """
    Start a scan on a connected device.

    Sends a command to a device via WebSocket to initiate a scan.

    Args
    ----
    device_id : str
        The unique identifier of the device.
    header_xml : str
        Metadata in XML format.
    sequence_data : str
        Data related to the scanning sequence.
    acquisition_data : str
        Data for scan acquisition.

    Raises
    ------
    HTTPException
        If the device is not found or not connected.

    """
    if not (await dal_get_device(device_id)):
        raise HTTPException(status_code=404, detail="Device not found")
    if device_id not in dict_id_websocket:
        raise HTTPException(status_code=404, detail="Device not connected")
    print("Start Scan")
    websocket = dict_id_websocket[device_id]
    data = {
        "header_xml" : header_xml,
        "sequence_data" : sequence_data,
        "acquisition_data": acquisition_data
    }
    await websocket.send_json({
        "command": "start",
        "data": data
    })

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

    print('Device connected.')

    device_id_global = ""

    try:
        while True:
            message = await websocket.receive_json()
            command = message.get('command')
            # ===============  Register device ===================
            if command == 'register':
                if device_id_global != "":
                    await websocket.send_json({'message': 'Error registering device. \
In this session a device already was registered.'})
                    continue
                device_data = message.get('data')
                device_id = device_data.get('id')
                device = DeviceOut(**device_data)

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
                    if "additional_data" in status_data:
                        additional_data = status_data.get('additional_data')
                        device_out.status = str({
                            "status": status_data.get('status'),
                            "additional_data": additional_data
                        })
                    else:
                        device_out.status = str({
                            "status": status_data.get('status'),
                        })
                    device_out.datetime_updated = datetime.now()
                    if not await dal_update_device(device_id, device_out):
                        await websocket.send_json({'message': 'Error updating device.'})
                    else:
                        # Send response to the device
                        await websocket.send_json({
                            'command': 'feedback',
                            'message': 'Device status updated successfully'})
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

    print('Device connected.')

    device_id_global = ""

    try:
        while True:
            message = await websocket.receive_json()
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
                device = DeviceOut(ip_address=ip_address, **device_data)
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
