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
import hashlib
from secrets import compare_digest, token_hex
from typing import Annotated, Dict, Optional
from uuid import UUID

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
async def websocket_endpoint(websocket: WebSocket):
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
            command = message.get('command')

            # ---------- Register device
            if command == 'register':
                await handle_register(websocket, message, device_id)

            # ---------- Update device status
            elif command == 'update_status':
                await handle_status_update(websocket, message, device_id)

            # ---------- Receive file/data from device
            elif command == 'file-transfer':
                await handle_file_transfer(websocket, message)

            else:
                await websocket.send_json({"command": "feedback", "message": f"Unknown command: {command}"})
                print("Received unknown command, which will be ignored:", command)


    except WebSocketDisconnect:
        print("WebSocketDisconnect")
        del dict_id_websocket[device_id]
        print('Device disconnected:', device_id)
        # Set the status of the disconnected device to "disconnected"
        if not await dal_update_device(device_id, {"status": "DISCONNECTED"}):
            print('Error updating device status to disconnected.')


async def handle_register(websocket: WebSocket, message: dict, device_id: UUID) -> None:
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


async def handle_status_update(websocket: WebSocket, message: dict, device_id: UUID) -> None:
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


async def handle_file_transfer(websocket: WebSocket, header: dict) -> None:
    # Preflight
    if DATA_LAKE_DIR is None:
        raise OSError("Missing `DATA_LAKE_DIRECTORY` environment variable.")
    if not os.path.exists(DATA_LAKE_DIR):
        raise IsADirectoryError("`DATA_LAKE_DIRECTORY` does not exist.")

    task_id: str = str(header["task_id"])
    user_access_token: str = str(header["user_access_token"])
    filename_in: str = os.path.basename(str(header.get("filename", "upload.bin")))
    size_bytes: int = int(header["size_bytes"])
    # content_type: str = header.get("content_type")
    header_sha256: Optional[str] = header.get("sha256")

    # Locate task & result directory
    task = exam_requests.get_task(task_id, user_access_token)

    result_directory = os.path.join(DATA_LAKE_DIR, str(task.workflow_id))
    os.makedirs(result_directory, exist_ok=True)

    # Create blank result entry
    blank_result = exam_requests.create_blank_result(task_id, user_access_token)

    # Preserve extension if present
    root, ext = os.path.splitext(filename_in)
    final_filename = f"{blank_result.id}{ext or ''}"
    file_path = os.path.join(result_directory, final_filename)
    tmp_path = file_path + ".part"

    # Receive bytes -> stream to disk
    hasher = hashlib.sha256()
    bytes_received = 0
    with open(tmp_path, "wb") as fout:
        while bytes_received < size_bytes:
            event = await websocket.receive()
            if event["type"] == "websocket.disconnect":
                raise WebSocketDisconnect(code=1001)
            if event["type"] != "websocket.receive":
                continue

            chunk = event.get("bytes")
            if chunk is None: # ignore stray text frames
                continue

            fout.write(chunk)
            hasher.update(chunk)
            bytes_received += len(chunk)

    # Check if we received the expected number of bytes
    if bytes_received != size_bytes:
        try:
            os.remove(tmp_path)
        except FileNotFoundError:
            pass
        await websocket.send_json({
            "command": "feedback",
            "message": f"Incomplete file received ({bytes_received}/{size_bytes} bytes).",
        })
        return

    # Checksum verification
    if header_sha256 and hasher.hexdigest() != header_sha256:
        try:
            os.remove(tmp_path)
        except FileNotFoundError:
            pass
        await websocket.send_json({
            "command": "feedback",
            "message": "Checksum mismatch for uploaded file.",
        })
        return

    os.replace(tmp_path, file_path)  # atomic finalize

    # Set result
    set_result = SetResult(
        type=_pick_result_type(filename_in),
        directory=result_directory,
        filename=final_filename,
    )
    result = exam_requests.set_result(str(blank_result.id), set_result, user_access_token)

    # Update task status to FINISHED
    task.status = ItemStatus.FINISHED
    _ = exam_requests.set_task(task_id, task, user_access_token)

    await websocket.send_json({
        "command": "feedback",
        "message": f"File {result.id} saved to datalake: {file_path}",
    })


def _pick_result_type(filename: str):
    """Map extensions to enum."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".dcm", ".dicom"]:
        return ResultType.DICOM
    elif ext in [".mrd"]:
        return ResultType.MRD
    elif ext in [".npy"]:
        return ResultType.NPY
    elif ext in [".json"]:
        return ResultType.CALIBRATION
    else:
        return ResultType.NOT_SET
