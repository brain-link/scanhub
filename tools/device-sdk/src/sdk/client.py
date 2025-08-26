"""Client module for managing device interactions with device-manager.

This module defines the `Client` class, which facilitates the connection,
device registration, and command handling for devices communicating with
device-manager via WebSocket.

Classes:
    Client: Handles device registration, status updates, and server command processing.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any, Optional

from scanhub_libraries.models import AcquisitionPayload, DeviceDetails, DeviceStatus

from sdk.websocket_handler import WebSocketHandler

CHUNK = 1 << 20  # 1 MiB, chunk size for file transfers

logging.basicConfig(level=logging.INFO)


class Client:
    """Client for managing WebSocket interactions with device-manager.

    Includes device registration, status updates, and handling server commands.

    Attributes
    ----------
        websocket_uri (str): The URI of the WebSocket server (device-manager).
        websocket_handler (WebSocketHandler): Manages the WebSocket connection.
        device_id (UUID): The Device ID. Copy it from Scanhub.
        device_token (str): The device-token used to authenticate the device. Copy it from Scanhub.
        details (DeviceDetails): Details about the device, including device paramters.
        reconnect_delay (int): Delay in seconds before reconnect attempts.
        feedback_handler (callable): Callback for handling feedback messages.
        scan_callback (callable): Callback for handling scanning commands.
        error_handler (callable): Callback for handling error messages.
        logger (logging.Logger): Logger for the class.

    """

    def __init__(
        self,
        websocket_uri: str,
        device_id: str,
        device_token: str,
        device_details: DeviceDetails,
        reconnect_delay: int = 5,
        ca_file: str | None = None,
    ) -> None:
        """Initialize the Client instance.

        Args:
        ----
            websocket_uri (str): URI of the WebSocket server (device-manager).
            device_id (UUID): The Device ID. Copy it from Scanhub.
            device_token (str): The device-token used to authenticate the device. Copy it from Scanhub.
            device_name (str): Name of the device.
            serial_number (str): Serial number of the device.
            manufacturer (str): Device manufacturer.
            modality (str): Device modality type.
            site (str): Device location.
            reconnect_delay (int, optional): Delay in seconds for reconnect attempts. Defaults to 5.
            ca_file (str | None): Filepath to a ca_file to verify the server.

        """
        self.websocket_uri = websocket_uri
        self.websocket_handler = WebSocketHandler(
            uri=websocket_uri,
            device_id=device_id,
            device_token=device_token,
            reconnect_delay=reconnect_delay,
            ca_file=ca_file,
        )
        self.device_id = device_id  # Unique ID for the device
        self.device_token = device_token
        self.details: DeviceDetails = device_details
        self.reconnect_delay = reconnect_delay
        # (Optional) Server feedback handler callback function
        self.feedback_handler: Optional[Callable[[str], Awaitable[None]]] = None
        # (Optional) Server error handler callback function
        self.error_handler: Optional[Callable[[str], Awaitable[None]]] = None
        # Acquisition callback function
        self.scan_callback: Optional[Callable[[AcquisitionPayload], Awaitable[None]]] = None

        # Initialize logger
        self.logger = logging.getLogger("DeviceClient")

    async def start(self) -> None:
        """Start the client by establishing a WebSocket connection.

        Registers the device and listening for incoming commands from the server.
        """
        await self.connect_and_register()
        asyncio.create_task(self.listen_for_commands())

    async def connect_and_register(self) -> None:
        """Connect to the WebSocket server and registers the device.

        Retries the connection and registration process upon failure after a delay.
        """
        await self.websocket_handler.connect()
        self.logger.info("WebSocket connection established.")
        await self.register_device()

    async def register_device(self) -> None:
        """Send a registration message to the server to register the device.

        The registration data includes device details like ID, name, manufacturer, and location.
        """
        registration_data = {
            "command": "register",
            "data": self.details.model_dump(),
        }
        await self.websocket_handler.send_message(json.dumps(registration_data))
        self.logger.info("Device registration sent.")

    async def listen_for_commands(self) -> None:
        """Listen for incoming commands from the server and processes them.

        Handles commands like 'start', 'feedback', and errors. Reconnects if the connection is lost.
        """
        while True:
            try:
                message = await self.websocket_handler.receive_message()
                if message is None:
                    # Connection closed, try to reconnect
                    raise ConnectionError("Connection lost. Attempting to reconnect...")
                data = json.loads(message)
                command = data.get("command")

                if command == "start":
                    payload = AcquisitionPayload(**data.get("data", {}))
                    await self.handle_start_command(payload)
                elif command == "feedback":  # for feedback only 'message' is needed
                    await self.handle_feedback(data.get("message"))
                else:  # on error whole websocket message is needed
                    await self.handle_error(str(data))
            except json.JSONDecodeError:
                self.logger.error("Received invalid JSON message: %s", message)
            except ConnectionError as e:
                if self.websocket_handler.websocket is None:
                    return  # No active connection, exit the loop
                self.logger.error(e)
                await self.reconnect()
            except Exception as e:
                self.logger.error("Error while receiving commands: %s", str(e))
                await self.reconnect()

    async def handle_start_command(self, payload: AcquisitionPayload) -> None:
        """Handle the 'start' command from the server to begin a scanning process.

        Sends an error status if the scan callback is not defined or an error occurs during processing.

        Args:
        ----
            deviceTask (dict): Command data containing scanning parameters.

        """
        try:
            if self.scan_callback:
                # Set device status to busy
                await self.send_status(status=DeviceStatus.BUSY)
                # Initialize scanning status (set to zero)
                await self.send_scanning_status(
                    progress=0, task_id=str(payload.id), user_access_token=payload.access_token,
                )
                # Call the external scan callback function
                await self.scan_callback(payload)
                # Set device status to ready
                await self.send_status(status=DeviceStatus.ONLINE)
            else:
                self.logger.error("Scan callback not defined.")
                await self.send_error_status("Scan callback not defined.")
        except Exception as exc:
            await self.send_error_status(
                error_message=str(exc), task_id=str(payload.id), user_access_token=payload.access_token,
            )
            self.logger.error("An error occurred while handling the start command: %s", str(exc))

    async def send_status(
        self,
        status: DeviceStatus,
        user_access_token: str | None = None,
        data: None | dict[str, Any] = None,
        task_id: str | None = None,
    ) -> None:
        """Send a status update to the server.

        Args:
        ----
            status (str): The status to report (e.g., 'scanning', 'ready', 'error').
            additional_data (dict, optional): Extra information to include with the status.

        """
        if not isinstance(status, DeviceStatus):
            raise TypeError("Invalid device status.")
        status_data = {
            "command": "update_status",
            "status": status.value,
            "data": data,
            "task_id": task_id,
            "user_access_token": user_access_token,
        }
        await self.websocket_handler.send_message(json.dumps(status_data))

    async def upload_file_result(self, file_path: str | Path, task_id: str, user_access_token: str) -> None:
        """Send MRD file as base64-encoded binary."""
        path = Path(file_path) if not isinstance(file_path, Path) else file_path
        if not path.exists():
            await self.send_error_status("Could not upload file", task_id=task_id, user_access_token=user_access_token)
            raise FileNotFoundError(f"File {file_path} does not exist.")

        try:
            size = path.stat().st_size
            ct = "application/x-ismrmrd+hdf5" if path.suffix == ".mrd" else "application/octet-stream"

            # Optional integrity: precompute sha256
            sha = hashlib.sha256()
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(CHUNK), b""):
                    sha.update(chunk)
            sha_hex = sha.hexdigest()

            header = {
                "command": "file-transfer",
                "task_id": task_id,
                "user_access_token": user_access_token,
                "filename": path.name,
                "size_bytes": size,
                "content_type": ct,
                "sha256": sha_hex,
            }
            await self.websocket_handler.send_message(json.dumps(header))  # metadata

            # stream file in binary frames
            with path.open("rb") as f:
                for chunk in iter(lambda: f.read(CHUNK), b""):
                    await self.websocket_handler.send_message(chunk)
            self.logger.info(f"Uploaded file {file_path} successfully!")
        except Exception as exc:
            await self.send_error_status(
                f"Could not upload file: {exc}", task_id=task_id, user_access_token=user_access_token,
            )
            raise

    async def send_scanning_status(
        self,
        progress: int,
        task_id: str,
        user_access_token: str,
    ) -> None:
        """Send a 'scanning' status with progress percentage.

        Args:
        ----
            progress (int): The scanning progress percentage.
            task_id (str): The task ID to report progress for.
            user_access_token (str): User access token.

        """
        await self.send_status(
            DeviceStatus.BUSY,
            data={"progress": progress},
            task_id=task_id,
            user_access_token=user_access_token,
        )

    async def send_error_status(
        self,
        error_message: str,
        task_id: str | None = None,
        user_access_token: str | None = None,
    ) -> None:
        """Send an 'error' status with a specific error message.

        Args:
        ----
            error_message (str): The error message to include.

        """
        if task_id is not None and user_access_token is not None:
            await self.send_status(
                DeviceStatus.ERROR,
                data={"error_message": error_message},
                task_id=task_id,
                user_access_token=user_access_token,
            )
        else:
            await self.send_status(
                DeviceStatus.ERROR, data={"error_message": error_message},
            )

    async def stop(self) -> None:
        """Close the WebSocket connection."""
        await self.websocket_handler.close()
        self.logger.info("WebSocket connection closed.")

    async def reconnect(self) -> None:
        """Reconnect to the server and re-registers the device.

        Waits for `reconnect_delay` seconds before attempting to reconnect.
        """
        self.logger.info("Attempting to reconnect in %d seconds...", self.reconnect_delay)
        await asyncio.sleep(self.reconnect_delay)
        await self.connect_and_register()

    async def handle_feedback(self, message: str) -> None:
        """Handle feedback messages from the server.

        Args:
        ----
            message (str): The feedback message.

        """
        if self.feedback_handler is not None:
            await self.feedback_handler(message)
        else:
            self.logger.info("Feedback received from server: %s", message)

    async def handle_error(self, message: str) -> None:
        """Handle error messages from the server.

        Args:
        ----
            message (str): The error message.

        """
        if self.error_handler is not None:
            await self.error_handler(message)
        else:
            self.logger.info("Error received from server: %s", message)

    def set_feedback_handler(self, handler: Callable[[str], Awaitable[None]]) -> None:
        """Set a callback function to handle feedback messages.

        Args:
        ----
            handler (callable): A function that takes a single string argument.

        """
        self.feedback_handler = handler

    def set_error_handler(self, handler: Callable[[str], Awaitable[None]]) -> None:
        """Set a callback function to handle error messages.

        Args:
        ----
            handler (callable): A function that takes a single string argument.

        """
        self.error_handler = handler

    def set_scan_callback(self, callback: Callable[[AcquisitionPayload], Awaitable[None]]) -> None:
        """Set a callback function to handle the scanning process.

        Args:
        ----
            callback (callable): A function that takes one argument (deviceTask).

        """
        self.scan_callback = callback
