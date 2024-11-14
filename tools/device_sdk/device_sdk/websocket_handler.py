# device_sdk/websocket_handler.py

import asyncio
import websockets
import logging

class WebSocketHandler:
    def __init__(self, uri, reconnect_delay=5):
        self.uri = uri
        self.websocket = None
        self.reconnect_delay = reconnect_delay
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        while True:
            try:
                self.websocket = await websockets.connect(self.uri)
                self.logger.info("WebSocket connection established.")
                break
            except Exception as e:
                self.logger.error(f"Failed to connect to WebSocket: {e}. Retrying in {self.reconnect_delay} seconds...")
                await asyncio.sleep(self.reconnect_delay)

    async def send_message(self, message):
        try:
            await self.websocket.send(message)
        except websockets.ConnectionClosed as e:
            self.logger.error(f"Failed to send message, connection closed: {e}")
            raise ConnectionError("Connection closed while trying to send a message.")

    async def receive_message(self):
        try:
            return await self.websocket.recv()
        except websockets.ConnectionClosed as e:
            self.logger.error(f"Connection closed: {e}")
            return None

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            self.logger.info("WebSocket connection closed.")