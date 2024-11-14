# device_sdk/client.py

import asyncio
import json
import logging
from .websocket_handler import WebSocketHandler

class Client:
    def __init__(self, websocket_uri, device_id, name, manufacturer, modality, status, site, ip_address, reconnect_delay=5):
        self.websocket_uri = websocket_uri
        self.websocket_handler = WebSocketHandler(websocket_uri)
        self.device_id = device_id  # Unique ID for the device
        self.name = name
        self.manufacturer = manufacturer
        self.modality = modality
        self.status = status
        self.site = site
        self.ip_address = ip_address
        self.reconnect_delay = reconnect_delay
        self.feedback_handler = None  # Optional callback for feedback
        self.scan_callback = None  # Callback for the scan process

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def start(self):
        await self.connect_and_register()
        asyncio.create_task(self.listen_for_commands())

    async def connect_and_register(self):
        while True:
            try:
                await self.websocket_handler.connect()
                self.logger.info("WebSocket connection established.")
                await self.register_device()
                break  # Exit loop if connection and registration are successful
            except Exception as e:
                self.logger.error(f"Failed to connect or register: {e}. Retrying in {self.reconnect_delay} seconds...")
                await asyncio.sleep(self.reconnect_delay)

    async def register_device(self):
        registration_data = {
            "command": "register",
            "data": {
                "id": self.device_id,  # Include device ID in the registration data
                "name": self.name,
                "manufacturer": self.manufacturer,
                "modality": self.modality,
                "status": self.status,
                "site": self.site,
                "ip_address": self.ip_address
            }
        }
        await self.websocket_handler.send_message(json.dumps(registration_data))
        self.logger.info("Device registration sent.")

    async def listen_for_commands(self):
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
                elif command == "feedback":
                    self.handle_feedback(data.get("message"))
                else:
                    self.handle_error(str(data))
            except json.JSONDecodeError:
                self.logger.error(f"Received invalid JSON message: {message}")
            except ConnectionError as e:
                self.logger.error(e)
                await self.reconnect()
            except Exception as e:
                self.logger.error(f"Error while receiving commands: {str(e)}")
                await self.reconnect()


    async def handle_start_command(self, data):
        try:
            if self.scan_callback:
                print(data)
                header_xml_str = data["header_xml"]
                sequence_data = data["sequence_data"]
                acquisition_data = data["acquisition_data"]
                # Call the external scan callback function
                await self.scan_callback(header_xml_str, sequence_data, acquisition_data)
            else:
                self.logger.error("Scan callback not defined.")
                await self.send_error_status("Scan callback not defined.")
        except Exception as e:
            await self.send_error_status(str(e))
            self.logger.error(f"An error occurred while handling the start command: {str(e)}")

    async def send_status(self, status, additional_data=None):
        status_data = {
            "command": "update_status",
            "data": {
                    "id": self.device_id,
                    "status": status
                }
            }
        if status == "scanning" and additional_data is not None:
            status_data["data"]["additional_data"] = {
                "percentage": additional_data
            }
        elif status == "error" and additional_data is not None:
            status_data["data"]["additional_data"] = {
                "error_message": additional_data
            }
        elif additional_data is not None:
            status_data["data"]["additional_data"] = additional_data
        await self.websocket_handler.send_message(json.dumps(status_data))

    async def send_scanning_status(self, percentage):
        await self.send_status("scanning", additional_data=percentage)

    async def send_ready_status(self):
        await self.send_status("ready")

    async def send_init_status(self):
        self.logger.info(f"send init status")
        await self.send_status("init")

    async def send_offline_status(self):
        await self.send_status("offline")

    async def send_error_status(self, error_message):
        await self.send_status("error", additional_data=error_message)

    async def stop(self):
        await self.websocket_handler.close()

    async def reconnect(self):
        self.logger.info(f"Attempting to reconnect in {self.reconnect_delay} seconds...")
        await asyncio.sleep(self.reconnect_delay)
        await self.connect_and_register()

    def handle_feedback(self, message):
        if self.feedback_handler:
            self.feedback_handler(message)
        else:
            self.logger.info(f"Feedback received from server: {message}")


    def handle_error(self, message):
        if self.error_handler:
            self.error_handler(message)
        else:
            self.logger.info(f"Error received from server: {message}")

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
            callback (callable): A function that takes three arguments (header_xml, sequence_data, acquisition_data).
        """
        self.scan_callback = callback