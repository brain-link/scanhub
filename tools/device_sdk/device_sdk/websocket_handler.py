"""
WebSocketHandler module for managing WebSocket connections.

This module provides the `WebSocketHandler` class, which simplifies managing a WebSocket connection, 
handling reconnection, and providing methods to send and receive messages.

Classes:
    WebSocketHandler: Manages WebSocket connections with reconnect logic.
"""

import asyncio
import logging
from websockets.asyncio.client import connect
from websockets.exceptions import InvalidURI, InvalidHandshake, InvalidStatus, ConnectionClosed


class WebSocketHandler:
    """
    A handler for managing WebSocket connections, sending and receiving messages,
    and handling automatic reconnection.

    Attributes:
        uri (str): The WebSocket server URI (device-manager) to connect to.
        websocket (websockets.WebSocketClientProtocol): The WebSocket connection object.
        device_id (str): The device ID to send when opening the connection.
        device_token (str): The device token to send when opening the connection.
        reconnect_delay (int): Delay in seconds before retrying connection upon failure.
        logger (logging.Logger): Logger instance for logging events.
    """
    def __init__(self, uri, device_id, device_token, reconnect_delay=5):
        """
        Initializes the WebSocketHandler instance.

        Args:
            uri (str): The URI of the WebSocket server (device-manager).
            reconnect_delay (int, optional): Time in seconds to wait before 
                                             retrying a failed connection. 
                                             Defaults to 5.
        """
        self.uri = uri
        self.device_id = device_id
        self.device_token = device_token
        self.websocket = None
        self.reconnect_delay = reconnect_delay
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """
        Establishes a WebSocket connection.

        Continuously attempts to connect to the WebSocket server specified by the URI.
        Retries connection after `reconnect_delay` seconds in case of failure.

        Logs specific connection-related errors and retries accordingly.
        """
        self.websocket = await connect(
            self.uri,
            additional_headers={
                "device-id": self.device_id,
                "device-token": self.device_token
            }
        )
        self.logger.info("WebSocket connection established.")

    async def send_message(self, message):
        """
        Sends a message through the WebSocket connection.

        Args:
            message (str): The message to be sent over the WebSocket.

        Raises:
            ConnectionError: If the WebSocket connection is closed during the send operation.
        """
        try:
            await self.websocket.send(message)
        except ConnectionClosed as e:
            self.logger.error("Failed to send message, connection closed: %s", e)
            raise ConnectionError("Connection closed while trying to send a message.") from e

    async def receive_message(self):
        """
        Receives a message from the WebSocket connection.

        Returns:
            str or None: The received message, or `None` if the connection is closed.

        Logs:
            Logs an error if the connection is closed.
        """
        try:
            return await self.websocket.recv()
        except ConnectionClosed as e:
            self.logger.error("Connection closed: %s", e)
            return None

    async def close(self):
        """
        Closes the WebSocket connection gracefully.

        Ensures the WebSocket connection is closed and logs the event.
        """
        if self.websocket:
            await self.websocket.close()
            self.logger.info("WebSocket connection closed.")
