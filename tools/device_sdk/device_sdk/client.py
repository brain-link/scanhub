"""
Client module for managing device interactions with device-manager.

This module defines the `Client` class, which facilitates the connection, 
device registration, and command handling for devices communicating with 
device-manager via WebSocket.

Classes:
    Client: Handles device registration, status updates, and server command processing.
"""

import asyncio
import json
import logging
from .websocket_handler import WebSocketHandler

class Client:
    """
    A client for managing WebSocket interactions with device-manager, including device registration,
    status updates, and handling server commands.

    Attributes:
        websocket_uri (str): The URI of the WebSocket server (device-manager).
        websocket_handler (WebSocketHandler): Manages the WebSocket connection.
        device_id (UUID): The Device ID. Copy it from Scanhub.
        device_token (str): The device-token used to authenticate the device. Copy it from Scanhub.
        name (str): Name of the device.
        manufacturer (str): Manufacturer of the device.
        modality (str): Device modality.
        site (str): Location of the device.
        ip_address (str): Device IP address.
        reconnect_delay (int): Delay in seconds before reconnect attempts.
        feedback_handler (callable): Callback for handling feedback messages.
        scan_callback (callable): Callback for handling scanning commands.
        error_handler (callable): Callback for handling error messages.
        logger (logging.Logger): Logger for the class.
    """
    def __init__(self, websocket_uri, device_id, device_token, name, manufacturer, modality, 
                 status, site, ip_address, reconnect_delay=5, ca_file=None):
        """
        Initializes the Client instance.

        Args:
            websocket_uri (str): URI of the WebSocket server (device-manager).
            device_id (UUID): The Device ID. Copy it from Scanhub.
            device_token (str): The device-token used to authenticate the device. Copy it from Scanhub.
            name (str): Name of the device.
            manufacturer (str): Device manufacturer.
            modality (str): Device modality type.
            site (str): Device location.
            ip_address (str): Device IP address.
            reconnect_delay (int, optional): Delay in seconds for reconnect attempts. Defaults to 5.
            ca_file (str | None): Filepath to a ca_file to verify the server.
        """
        self.websocket_uri = websocket_uri
        self.websocket_handler = WebSocketHandler(websocket_uri, device_id, device_token, ca_file=ca_file)
        self.device_id = device_id  # Unique ID for the device
        self.device_token = device_token
        self.name = name
        self.manufacturer = manufacturer
        self.modality = modality
        self.site = site
        self.ip_address = ip_address
        self.reconnect_delay = reconnect_delay
        self.feedback_handler = None  # Optional callback for feedback
        self.error_handler = None  # Optional callback for error
        self.scan_callback = None  # Callback for the scan process

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def start(self):
        """
        Starts the client by establishing a WebSocket connection, registering the device,
        and listening for incoming commands from the server.
        """
        await self.connect_and_register()
        asyncio.create_task(self.listen_for_commands())

    async def connect_and_register(self):
        """
        Connects to the WebSocket server and registers the device.

        Retries the connection and registration process upon failure after a delay.
        """
        await self.websocket_handler.connect()
        self.logger.info("WebSocket connection established.")
        await self.register_device()

    async def register_device(self):
        """
        Sends a registration message to the server to register the device.

        The registration data includes device details like ID, name, manufacturer, and location.
        """
        registration_data = {
            "command": "register",
            "data": {
                "status": 'REGISTERED',
                "name": self.name,
                "manufacturer": self.manufacturer,
                "modality": self.modality,
                "site": self.site,
                "ip_address": self.ip_address
            }
        }
        await self.websocket_handler.send_message(json.dumps(registration_data))
        self.logger.info("Device registration sent.")

    async def listen_for_commands(self):
        """
        Listens for incoming commands from the server and processes them.

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
                    await self.handle_start_command(data.get("data"))
                elif command == "feedback": # for feedback only 'message' is needed
                    await self.handle_feedback(data.get("message"))
                else: # on error whole websocket message is needed
                    await self.handle_error(str(data))
            except json.JSONDecodeError:
                self.logger.error("Received invalid JSON message: %s",
                                  message)
            except ConnectionError as e:
                self.logger.error(e)
                await self.reconnect()
            except Exception as e:
                self.logger.error("Error while receiving commands: %s",
                                  str(e))
                await self.reconnect()


    async def handle_start_command(self, deviceTask):
        """
        Handles the 'start' command from the server to begin a scanning process.

        Args:
            deviceTask (dict): Command data containing scanning parameters.

        Sends an error status if the scan callback is not defined or an error 
        occurs during processing.
        """
        try:
            if self.scan_callback:
                # Call the external scan callback function
                await self.scan_callback(deviceTask)
            else:
                self.logger.error("Scan callback not defined.")
                await self.send_error_status("Scan callback not defined.")
        except Exception as e:
            await self.send_error_status(str(e))
            self.logger.error("An error occurred while handling the start command: %s",
                              str(e))

    async def send_status(self, status, data=None, record_id=None, user_access_token=None):
        """
        Sends a status update to the server.

        Args:
            status (str): The status to report (e.g., 'scanning', 'ready', 'error').
            additional_data (dict, optional): Extra information to include with the status.
        """
        status_data = {
            "command": "update_status",
            "status": status,
            "data": data,
            "record_id": record_id,
            "user_access_token": user_access_token
        }
        await self.websocket_handler.send_message(json.dumps(status_data))

    async def send_scanning_status(self, progress, record_id, user_access_token):
        """
        Sends a 'scanning' status with progress percentage.

        Args:
            progress (int): The scanning progress percentage.
            record_id (str): The record_id to report progress for.
        """
        await self.send_status("SCANNING", data={'progress': progress}, record_id=record_id, user_access_token=user_access_token)

    async def send_ready_status(self):
        """Sends a 'ready' status to the server."""
        await self.send_status("READY")

    async def send_error_status(self, error_message):
        """
        Sends an 'error' status with a specific error message.

        Args:
            error_message (str): The error message to include.
        """
        await self.send_status("ERROR", data={'error_message': error_message})

    async def stop(self):
        """Closes the WebSocket connection."""
        await self.websocket_handler.close()

    async def reconnect(self):
        """
        Reconnects to the server and re-registers the device.

        Waits for `reconnect_delay` seconds before attempting to reconnect.
        """
        self.logger.info("Attempting to reconnect in %d seconds...",
                         self.reconnect_delay)
        await asyncio.sleep(self.reconnect_delay)
        await self.connect_and_register()

    async def handle_feedback(self, message):
        """
        Handles feedback messages from the server.

        Args:
            message (str): The feedback message.
        """
        if self.feedback_handler:
            await self.feedback_handler(message)
        else:
            self.logger.info("Feedback received from server: %s",
                             message)

    async def handle_error(self, message):
        """
        Handles error messages from the server.

        Args:
            message (str): The error message.
        """
        if self.error_handler:
            await self.error_handler(message)
        else:
            self.logger.info("Error received from server: %s",
                             message)

    def set_feedback_handler(self, handler):
        """
        Set a callback function to handle feedback messages.

        Args:
            handler (callable): A function that takes a single string argument.
        """
        self.feedback_handler = handler

    def set_error_handler(self, handler):
        """
        Set a callback function to handle error messages.

        Args:
            handler (callable): A function that takes a single string argument.
        """
        self.error_handler = handler

    def set_scan_callback(self, callback):
        """
        Set a callback function to handle the scanning process.

        Args:
            callback (callable): A function that takes one 
            argument (deviceTask).
        """
        self.scan_callback = callback
