"""
Device websocket connection.

This module defines the WebSocket endpoints for managing devices.
It includes functionalities for:
- Device registration and status updates via WebSocket.
- Listening for commands from devices.

Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""
import asyncio
import hashlib
import json
import os
import time
from pathlib import Path
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
    DeviceStatus,
    ItemStatus,
    ResultType,
    SetResult,
)
from scanhub_libraries.security import compute_complex_password_hash
from sqlalchemy import exc

import app.api.exam_requests as exam_requests
from app.api.dal import dal_get_device, dal_update_device

LOG_CALL_DELIMITER = "-------------------------------------------------------------------------------"
DATA_LAKE_DIR = os.getenv("DATA_LAKE_DIRECTORY")
DAGSTER_GRAPHQL_URL = "http://dagster-webserver:3000/dagster/graphql"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter()

# Maintain active WebSocket connections and a mapping of device IDs to WebSockets
dict_id_websocket: Dict[UUID, WebSocket] = {}

# Maintain device parameters from acquisition start
# dict_id_parameters: dict[UUID, dict] = {}

# Maintain latest device activity (pong)
device_last_seen: Dict[UUID, float] = {}


async def send_json(websocket, payload: dict):
    """Send json payload via websocket."""
    try:
        await websocket.send_json(payload)
    except WebSocketDisconnect:
        # Socket is already closed — just log and ignore
        print("WebSocket already closed, cannot send:", payload)
    except RuntimeError as exc:
        # Starlette sometimes raises RuntimeError when send called after close
        print(f"RuntimeError while sending WS message: {exc}")


@router.post("/trigger_acquisition/{task_id}", response_model={}, status_code=200, tags=["devices"])
async def trigger_acquisition(
    task_id: UUID,
    access_token: Annotated[str, Depends(oauth2_scheme)],
):
    """Trigger an MRI acquisition for the given task.

    Fetches the task from the exam manager, looks up the assigned sequence and device,
    sends the scan-start command via the device's open WebSocket, and marks the task as STARTED.
    """
    task = exam_requests.get_task(str(task_id), access_token)

    if task.sequence_id is None:
        raise HTTPException(status_code=400, detail="Missing sequence ID on task.")
    if task.device_id is None:
        raise HTTPException(status_code=400, detail="Missing device ID on task.")

    if task.device_id not in dict_id_websocket:
        raise HTTPException(status_code=503, detail="Device offline.")

    sequence = exam_requests.get_sequence(task.sequence_id, access_token)

    if not (device := await dal_get_device(task.device_id)):
        raise HTTPException(status_code=404, detail="Device not found.")
    device_details = DeviceDetails(**device.__dict__)

    payload = AcquisitionPayload(
        **task.model_dump(),
        sequence=sequence,
        mrd_header="header_xml_placeholder",
        access_token=access_token,
        device_parameter=device_details.parameter or {},
    )

    websocket = dict_id_websocket[task.device_id]
    await websocket.send_text(
        json.dumps({"command": "start", "data": payload}, default=jsonable_encoder)
    )

    exam_requests.update_task_status(str(task_id), "STARTED", access_token)
    return {}


async def connection_with_valid_id_and_token(websocket: WebSocket) -> UUID:
    """Check if the given device_id and device_token belong to an existing device in the database."""
    device_id_header = websocket.headers.get("device-id")
    device_token = websocket.headers.get("device-token")
    print(LOG_CALL_DELIMITER)
    print("Device ID:", device_id_header, "\nDevice token:", device_token)

    if not device_id_header or not device_token:
        print("Invalid device_id or device_token:", device_id_header, device_token)
        raise WebSocketException(code=1008, reason="Invalid device_id or device_token")
    try:
        device_id = UUID(device_id_header)
    except ValueError:
        print("Invalid device_id format:", device_id_header)
        raise WebSocketException(code=1008, reason="Invalid device_id")

    if not (device := await dal_get_device(device_id)):
        # do the same steps as if user existed to avoid disclosing info about existence of users
        dummy_hash = compute_complex_password_hash(device_token, token_hex(1024))
        compare_digest(dummy_hash, dummy_hash)
        print("Invalid device_id:", device_id)
        raise WebSocketException(code=1008, reason="Invalid device_id or device_token")

    # check token for user
    received_token_hash = compute_complex_password_hash(device_token, device.salt)
    token_match = compare_digest(received_token_hash, device.token_hash)
    if not token_match:
        print("Invalid device_token", device_token, "for device_id", device_id)
        raise WebSocketException(code=1008, reason="Invalid device_id or device_token")

    return device_id

# The dependency on get_current_user that is declared at the creation of the router does not inherit to this websocket
# but only to regular http endpoints.
# pylint: disable=locally-disabled, too-many-branches
# TODO improve overall logic and resilience


# Coroutine to monitor device status depending on ping-pong
async def monitor_devices():
    """Monitor device online/offline status."""
    while True:
        now = time.time()
        for dev, last_seen in device_last_seen.items():
            if now - last_seen > 60:  # 1 minute timeout
                await dal_update_device(dev, {"status": DeviceStatus.OFFLINE})
        await asyncio.sleep(30)


@router.websocket("/ws")
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
    print("Device connected on websocket.")
    try:
        dict_id_websocket[device_id] = websocket
        while True:
            message = await websocket.receive_json()
            command = message.get("command")

            # ---------- Register device
            if command == "register":
                await handle_register(websocket, message, device_id)

            # ---------- Response to heartbeat
            elif command == "ping":
                device_last_seen[device_id] = time.time()
                await send_json(websocket, {"command": "pong"})

            # ---------- Update device status
            elif command == "update_status":
                await handle_status_update(websocket, message, device_id)

            # ---------- Receive file/data from device
            elif command == "file-transfer":
                await handle_file_transfer(websocket, message, device_id)

            else:
                await send_json(websocket, {"command": "feedback", "message": f"Unknown command: {command}"})
                print("Received unknown command, which will be ignored:", command)

            command = None  # Reset command to avoid confusion in the next iteration

    except WebSocketDisconnect:
        print("WebSocketDisconnect")
        dict_id_websocket.pop(device_id, None)
        # dict_id_parameters.pop(device_id, None)
        print("Device disconnected:", device_id)
        # Set the status of the disconnected device to "disconnected"
        if not await dal_update_device(device_id, {"status": DeviceStatus.OFFLINE}):
            print("Error updating device status to disconnected.")


async def handle_register(websocket: WebSocket, message: dict, device_id: UUID) -> None:
    """Handle device registration."""
    print("Handle command 'register'.")
    try:
        device_details = message.get("data")
        if not isinstance(device_details, dict):
            await send_json(websocket, {"message": "Invalid device details."})
            return
        device_details_object = DeviceDetails(**device_details)
        device_details_object.status = DeviceStatus.ONLINE
        await dal_update_device(device_id, device_details_object.model_dump())
        print("Device registered.")
        # Send response to the device
        await send_json(websocket, {
            "command": "feedback",
            "message": "Device registered successfully"})
    except exc.SQLAlchemyError as exception:
        print("Error registering device: ", exception)
        await send_json(websocket, {"message": "Error registering device" + str(exception)})


async def handle_status_update(websocket: WebSocket, message: dict, device_id: UUID) -> None:
    """Handle device status updates from the device SDK."""
    print("Handle device status update...")

    # Parse and validate status
    status_str = str(message.get("status"))
    try:
        status = DeviceStatus(status_str)
    except ValueError:
        await send_json(websocket, {
            "command": "feedback",
            "message": f"Invalid status: {status_str}"
        })
        return

    # Update the device's current state in the DB
    if not await dal_update_device(device_id, {"status": status}):
        print("Error updating device, device_id:", device_id)
        await send_json(websocket, {
            "command": "feedback",
            "message": "Error updating device state."
        })

    # Handle task-specific updates only when required
    # For ONLINE/OFFLINE states, we don't expect a task_id or token
    if status in (DeviceStatus.ONLINE, DeviceStatus.OFFLINE):
        await send_json(websocket, {
            "command": "feedback",
            "message": f"Device {status.value.upper()} acknowledged.",
        })
        return


    # For BUSY or ERROR, these identifiers are required
    task_id = message.get("task_id")
    user_access_token = message.get("user_access_token")
    if not task_id or not user_access_token:
        await send_json(websocket, {
            "command": "feedback",
            "message": "Missing task_id or user_access_token for task update."
        })
        return

    # Retrieve and update the acquisition task
    try:
        task = exam_requests.get_task(str(task_id), str(user_access_token))
    except Exception as exc:
        await send_json(websocket, {
            "command": "feedback",
            "message": f"Error fetching task: {exc}"
        })
        return

    if not task:
        await send_json(websocket, {
            "command": "feedback",
            "message": f"Task not found for ID: {task_id}"
        })
        return

    # Apply task state logic depending on device status
    data = message.get("data", {})
    if status == DeviceStatus.ERROR:
        task.status = ItemStatus.ERROR
        task.progress = task.progress or 0
        error_message = data.get("error_message", "Unspecified device error.")
        print(f"Device reported ERROR: {error_message}")

    elif status == DeviceStatus.BUSY:
        progress = int(data.get("progress", task.progress or 0))
        task.progress = max(0, min(progress, 100))
        if task.progress >= 100:
            task.status = ItemStatus.FINISHED
        else:
            task.status = ItemStatus.INPROGRESS

    # Persist and send feedback
    try:
        updated_task = exam_requests.set_task(str(task_id), task, str(user_access_token))
        await send_json(websocket, {
            "command": "feedback",
            "message": f"Device {status.value} update processed (progress={updated_task.progress}%)."
        })
    except Exception as exc:
        await send_json(websocket, {
            "command": "feedback",
            "message": f"Could not update task: {exc}"
        })


async def _stream_to_file(websocket: WebSocket, tmp_path: Path, size_bytes: int) -> tuple[int, str]:
    """Stream bytes from a WebSocket into a temp file; returns (bytes_received, sha256_hex)."""
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
            if chunk is None:
                continue
            fout.write(chunk)
            hasher.update(chunk)
            bytes_received += len(chunk)
    return bytes_received, hasher.hexdigest()


def _submit_reconstruction_job(task_id: str, task_dir: str, protocol_id: str, user_access_token: str) -> None:
    """Submit the mrpro_reconstruction_job to Dagster after a file transfer completes."""
    try:
        from dagster_graphql import DagsterGraphQLClient  # noqa: PLC0415
        from gql.transport.requests import RequestsHTTPTransport  # noqa: PLC0415
        _transport = RequestsHTTPTransport(
            url=DAGSTER_GRAPHQL_URL, use_json=True, timeout=30,
        )
        client = DagsterGraphQLClient(hostname="dagster-webserver", port_number=3000, transport=_transport)
        run_config = {
            "resources": {
                "dag_config": {
                    "config": {
                        "task_dir": task_dir,
                        "task_id": task_id,
                        "protocol_id": protocol_id,
                        "user_access_token": user_access_token,
                    },
                },
            },
        }
        client.submit_job_execution("mrpro_reconstruction_job", run_config=run_config)
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: Failed to submit Dagster reconstruction job: {exc}")  # noqa: T201


async def handle_file_transfer(websocket: WebSocket, header: dict, device_id: UUID) -> None:
    """Handle file transfer from device to server."""
    if DATA_LAKE_DIR is None:
        msg = "Missing `DATA_LAKE_DIRECTORY` environment variable."
        raise OSError(msg)
    if not Path(DATA_LAKE_DIR).exists():
        msg = "`DATA_LAKE_DIRECTORY` does not exist."
        raise IsADirectoryError(msg)

    task_id: str = str(header["task_id"])
    user_access_token: str = str(header["user_access_token"])
    filename: Path = Path(header.get("filename", "upload.bin"))
    size_bytes: int = int(header["size_bytes"])
    header_sha256: str | None = header.get("sha256")
    device_parameter: dict | None = header.get("device_parameter")

    task = exam_requests.get_task(task_id, user_access_token)
    task_dir = Path(DATA_LAKE_DIR) / str(task.protocol_id) / str(task_id)
    task_dir.mkdir(exist_ok=True, parents=True)
    file_path = task_dir / filename
    tmp_path = file_path.with_suffix(file_path.suffix + ".part")

    bytes_received, hexdigest = await _stream_to_file(websocket, tmp_path, size_bytes)

    if bytes_received != size_bytes:
        tmp_path.unlink(missing_ok=True)
        await send_json(websocket, {
            "command": "feedback",
            "message": f"Incomplete file received ({bytes_received}/{size_bytes} bytes).",
        })
        return

    if header_sha256 and hexdigest != header_sha256:
        tmp_path.unlink(missing_ok=True)
        await send_json(websocket, {
            "command": "feedback",
            "message": "Checksum mismatch for uploaded file.",
        })
        return

    tmp_path.replace(file_path)
    result_files = [file_path.name]

    if device_parameter:
        parameter_path = task_dir / "device_parameter.json"
        with parameter_path.open("w") as fh:
            json.dump({"device_id": str(device_id), "parameter": device_parameter}, fh, indent=4)
        result_files.append(parameter_path.name)

    blank_result = exam_requests.create_blank_result(task_id, user_access_token)
    set_result_payload = SetResult(
        type=_pick_result_type(file_path.name),
        directory=str(task_dir),
        files=result_files,
    )
    result = exam_requests.set_result(str(blank_result.id), set_result_payload, user_access_token)

    _submit_reconstruction_job(
        task_id=task_id,
        task_dir=str(task_dir),
        protocol_id=str(task.protocol_id),
        user_access_token=user_access_token,
    )

    await send_json(websocket, {
        "command": "feedback",
        "message": f"File saved and reconstruction triggered: {file_path}",
        "result_id": str(result.id),
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
