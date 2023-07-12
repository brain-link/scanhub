# Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

"""Device api endpoints."""
# TODO: Work on database instead of local list
# pylint: disable=no-name-in-module

from typing import List

from datetime import datetime, timedelta
from fastapi import APIRouter, WebSocket, HTTPException
import websockets
from .models import DeviceOut, get_device_out

from .dal import (
    dal_create_device,
    dal_delete_device,
    dal_get_all_devices,
    dal_get_device,
    dal_update_device,
)

router = APIRouter()


@router.get("/health/readiness", response_model={}, status_code=200, tags=["health"])
async def readiness() -> dict:
    """Readiness health endpoint.

    Returns
    -------
        Status dictionary
    """
    return {"status": "ok"}


@router.get('/devices', response_model=List[DeviceOut], status_code=200, tags=["devices"])
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


@router.get('/devices/{device_id}/ip_address')
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


@router.get('/devices/{device_id}', response_model=DeviceOut, status_code=200, tags=["devices"])
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


@router.get('/devices/{device_id}/status')
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


    # Check if the stored status is outdated (e.g., older than 1 hour)
    if device.datetime_updated < datetime.now() - timedelta(hours=1):
        # Send request for current status over the WebSocket connection
        websocket = await create_websocket_connection(device.ip_address)
        await websocket.send_json({'command': 'get_status'})
        response = await websocket.receive_json()
        current_status = response.get('status')
        await websocket.close()

        device_out = await get_device_out(device)
        # Update the device's status and last_status_update
        device_out.status = current_status
        device_out.datetime_updated = datetime.now()
        if not (device_new := await dal_update_device(device_id, device_out)):
            raise HTTPException(status_code=404, detail="Error updating device in db")

    # Return the current status of the device
    return {'status': device_new.status}


@router.delete('/devices/{device_id}', response_model={}, status_code=204, tags=["devices"])
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


async def create_websocket_connection(ip_address: str) -> WebSocket:
    """
    Create a WebSocket connection to the specified IP address.

    Args
    -------
        ip_address (str): The IP address of the device.

    Returns
    -------
        WebSocket: The WebSocket connection object.
    """
    websocket_url = f"ws://{ip_address}/ws"  # Assuming WebSocket endpoint is /ws
    return await websockets.client.connect(websocket_url)


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket endpoint for device communication.

    Args
    ----
        websocket (WebSocket): The WebSocket connection object.
    """
    await websocket.accept()
    print('Device connected:', websocket.client.host)

    try:
        while True:
            message = await websocket.receive_json()
            command = message.get('command')
            if command == 'register':
                device_data = message.get('data')
                ip_address = websocket.client.host
                device_id = device_data.get('id')
                device = DeviceOut(id=device_id, ip_address=ip_address, **device_data)
                if not (device := await dal_create_device(device)):
                    print('Error registering device: ', device)
                    await websocket.send_json({'message': 'Error registering device'})
                else:
                    print('Device registered:', device)
                    # Send response to the device
                    await websocket.send_json({'message': 'Device registered successfully'})

            elif command == 'update_status':
                status_data = message.get('data')
                ip_address = websocket.client.host
                if not (device := await dal_get_device(status_data.get('id'))):
                    await websocket.send_json({'message': 'Device not registered'})
                else:
                    if not (device_new := await dal_update_device(device_id, device)):
                        await websocket.send_json({'message': 'Error updating device.'})
                    else:
                        # Send response to the device
                        await websocket.send_json({'message': f'Device status updated successfully, {device_new}'})

    except websockets.exceptions.ConnectionClosedOK:
        print('Device disconnected:', websocket.client.host)
        # Set the status of the disconnected device to "disconnected"
        # TODO: don't use ip to identify
        # for device in devices:
        #     if device.ip_address == websocket.client.host:
        #         device.status = 'disconnected'
        #         device.last_status_update = datetime.now()
        #         print('Device status updated:', device)
        #         break
        # else:
        #     print('Device not found:', websocket.client.host)
            