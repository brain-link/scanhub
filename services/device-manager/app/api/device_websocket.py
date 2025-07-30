"""
Device websocket connection.

This module defines the WebSocket endpoints for managing devices.
It includes functionalities for:
- Device registration and status updates via WebSocket.
- Listening for commands from devices.

Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""
import base64
import json
import os
from secrets import compare_digest, token_hex
from typing import Annotated, Dict
from uuid import UUID

import numpy as np
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
)
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    AcquisitionPayload,
    AcquisitionTaskOut,
    DeviceDetails,
    ItemStatus,
    ResultType,
    SetResult,
)
from scanhub_libraries.security import compute_complex_password_hash
from sqlalchemy import exc

import app.api.exam_requests as exam_requests
from app.api.dal import (
    dal_get_device,
    dal_update_device,
)

LOG_CALL_DELIMITER = "-------------------------------------------------------------------------------"
DATA_LAKE_DIR = os.getenv("DATA_LAKE_DIRECTORY")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

# Maintain active WebSocket connections and a mapping of device IDs to WebSockets
dict_id_websocket: Dict[UUID, WebSocket] = {}


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
    # Get pulseq sequence
    sequence = exam_requests.get_sequence(task.sequence_id, access_token)

    payload = AcquisitionPayload(
        **task.model_dump(),
        sequence=sequence,
        mrd_header="header_xml_placeholder",  # Placeholder, should be filled with actual MRD header
        access_token=access_token,
    )

    if task.device_id in dict_id_websocket:
        websocket = dict_id_websocket[task.device_id]
        await websocket.send_text(
            json.dumps(
                {'command': 'start', 'data': payload},
                default=jsonable_encoder
            ))
        return
    else:
        raise HTTPException(status_code=503, detail='Device offline.')


async def connection_with_valid_id_and_token(websocket: WebSocket) -> UUID:
    """Check if the given device_id and device_token belong to an existing device in the database."""
    device_id_header = websocket.headers.get('device-id')
    device_token = websocket.headers.get('device-token')
    print(LOG_CALL_DELIMITER)
    print("Device ID:", device_id_header, "\nDevice token:", device_token)

    if not device_id_header or not device_token:
        print('Invalid device_id or device_token:', device_id_header, device_token)
        raise WebSocketException(code=1008, reason='Invalid device_id or device_token')
    try:
        device_id = UUID(device_id_header)
    except ValueError:
        print('Invalid device_id format:', device_id)
        raise WebSocketException(code=1008, reason='Invalid device_id')

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
async def websocket_endpoint(
    websocket: WebSocket,
    # device_id: Annotated[UUID, Depends(connection_with_valid_id_and_token)]
):
    """
    Websocket endpoint for device communication.

    Args
    ----
        websocket (WebSocket): The WebSocket connection object.
        device_id (UUID): The device_id.
    """
    await websocket.accept()
    device_id = await connection_with_valid_id_and_token(websocket)
    print('Device connected on websocket.')
    try:
        dict_id_websocket[device_id] = websocket
        while True:
            message = await websocket.receive_json()
            # print("Received messgage:", message)
            command = message.get('command')
            # ===============  Register device ===================
            if command == 'register':
                print("Handle command 'register'.")
                try:
                    device_details = message.get('data')
                    device_details_object = DeviceDetails(**device_details)
                    await dal_update_device(device_id, device_details_object.model_dump())
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

                if status == 'SCANNING':
                    # Get task
                    task_id = str(message.get('task_id'))
                    user_access_token = str(message.get('user_access_token'))
                    task = exam_requests.get_task(task_id, user_access_token)
                    task.progress = data['progress']
                    updated_task = exam_requests.set_task(task_id, task, user_access_token)
                    await websocket.send_json({
                        'command': 'feedback',
                        'message': f'Acquisition task progress: {updated_task.progress}%',
                    })

                await websocket.send_json({
                    'command': 'feedback',
                    'message': 'Device status updated.'
                })

            elif command == 'result':
                print("Handle command 'result'.")
                # Check data lake
                if DATA_LAKE_DIR is None:
                    raise OSError("Missing `DATA_LAKE_DIRECTORY` environment variable.")
                if not os.path.exists(DATA_LAKE_DIR):
                    raise IsADirectoryError("`DATA_LAKE_DIRECTORY` does not exist.")
                # Get the result data from the message
                shape = tuple(message.get('shape'))
                dtype = message.get('dtype')
                array_bytes = base64.b64decode(message.get('data'))
                result_data = np.frombuffer(array_bytes, dtype=dtype).reshape(shape)
                print(f"Received result with shape {result_data.shape} and dtype {result_data.dtype}")

                # Get corresponding acquisition task
                task_id = str(message.get('task_id'))
                user_access_token = str(message.get('user_access_token'))
                task = exam_requests.get_task(task_id, user_access_token)

                # Update task status to FINISHED
                task.status = ItemStatus.FINISHED
                _ = exam_requests.set_task(task_id, task, user_access_token)

                # Define result directory
                result_directory = os.path.join(DATA_LAKE_DIR, str(task.workflow_id))
                os.makedirs(result_directory, exist_ok=True)
                print(f"Saving to data lake directory: {result_directory}")

                # Create blank result
                blank_result = exam_requests.create_blank_result(task_id, user_access_token)
                # Update result info with created ID
                set_result = SetResult(
                    type=ResultType.NPY,
                    directory=result_directory,
                    filename=f"{blank_result.id}.npy",
                )

                # Save result to shared datalake
                file_path = os.path.join(set_result.directory, set_result.filename)
                np.save(file_path, result_data)

                if os.path.exists(file_path):
                    result = exam_requests.set_result(str(blank_result.id), set_result, user_access_token)
                    print("Result in database: ", result.model_dump())
                    # Send feedback to the device
                    await websocket.send_json({
                        'command': 'feedback',
                        'message': f'Result {result.id} saved successfully to datalake: {file_path}',
                    })
                else:
                    exam_requests.delete_blank_result(str(blank_result.id), user_access_token)
                    await websocket.send_json({
                        'command': 'feedback',
                        'message': f'Could not save result {result.id}, removing blank result from database...',
                    })

            else:
                print("Received unknown command, which will be ignored:", command)

    except WebSocketDisconnect:
        print("WebSocketDisconnect")
        del dict_id_websocket[device_id]
        print('Device disconnected:', device_id)
        # Set the status of the disconnected device to "disconnected"
        if not await dal_update_device(device_id, {"status": "DISCONNECTED"}):
            print('Error updating device status to disconnected.')
