"""
Device API Endpoints.

This module defines the API routes and WebSocket endpoints for managing devices.
It includes functionalities for:
- CRUD operations on devices.
- Device registration and status updates via WebSocket.

Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
"""
import io
import json
from secrets import token_hex
from typing import Annotated, List
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from scanhub_libraries.models import (
    DeviceCreationRequest,
    DeviceOut,
    User,
    DeviceStatus
)
from scanhub_libraries.security import compute_complex_password_hash, get_current_user

from app.api.dal import (
    dal_create_device,
    dal_delete_device,
    dal_get_all_devices,
    dal_get_device,
    dal_update_device,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

LOG_CALL_DELIMITER = "-------------------------------------------------------------------------------"


# The dependency on get_current_user that is declared here does not inherit
# to websockets but only to regular http endpoints.
router = APIRouter()


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
    return [DeviceOut(**device.__dict__) for device in devices_all]


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
    # print(LOG_CALL_DELIMITER)
    # print("Username:", current_user.username)
    # print("Device-ID:", device_id)
    if not (device := await dal_get_device(device_id)):
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceOut(**device.__dict__)


@router.post("/createdevice", status_code=201, tags=["devices"])
async def create_device(
    current_user: Annotated[User, Depends(get_current_user)],
    request: DeviceCreationRequest,
) -> StreamingResponse:
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

    if len(request.name) < 1:
        raise HTTPException(
            status_code=400,
            detail="The device name must not be empty!")
    if len(request.description) < 1:
        raise HTTPException(
            status_code=400,
            detail="The description name must not be empty!")
    request.status = DeviceStatus.OFFLINE

    device_token = token_hex(1024)  # create new token
    salt = token_hex(1024)  # create new salt
    hashed_token = compute_complex_password_hash(device_token, salt)
    device = await dal_create_device(request, hashed_token, salt)

    # Create temporary file with device credentials
    token_dict = {"device_token": device_token, "device_id": str(device.id)}
    # Convert to JSON and write to an in-memory file
    json_bytes = json.dumps(token_dict, indent=2).encode("utf-8")
    file_like = io.BytesIO(json_bytes)

    # Create response with headers for download
    return StreamingResponse(
        file_like,
        media_type="application/json",
        headers={
            "Content-Disposition": 'attachment; filename="device_credentials.json"'
        }
    )


@router.delete('/{device_id}', response_model={}, status_code=204, tags=["devices"])
async def delete_device(device_id: UUID, current_user: Annotated[User, Depends(get_current_user)]):
    """
    Delete a device.

    Args
    -------
        device_id (str): The ID of the device.

    Returns
    -------
        dict: The response indicating the success or failure of the deletion.
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", current_user.username)
    if not await dal_delete_device(device_id):
        raise HTTPException(status_code=404, detail="Device not found")

@router.put(
    "/parameter/{device_id}",
    response_model=DeviceOut,
    status_code=200,
    tags=["devices"],
    summary="Update acquisition/device parameter",
)
async def update_device_parameter(
    device_id: UUID | str,
    payload: dict,
    user: Annotated[User, Depends(get_current_user)],
) -> DeviceOut:
    """Update acquisition/device parameter.

    Parameters
    ----------
    device_id
        Id of the device to be updated
    payload
        Parameter dictionary

    Returns
    -------
        Parameter dictionary

    Raises
    ------
    HTTPException
        404: Not found
    """
    print(LOG_CALL_DELIMITER)
    print("Username:", user.username)
    print("Device ID:", device_id)
    _id = UUID(device_id) if not isinstance(device_id, UUID) else device_id
    print(f"Received payload: {payload}")
    if not (updated_device := await dal_update_device(device_id=_id, payload={"parameter": payload})):
        message = "Could not update exam, either because it does not exist, or for another reason."
        raise HTTPException(status_code=404, detail=message)
    return DeviceOut(**updated_device.__dict__)
