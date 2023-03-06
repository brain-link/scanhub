import logging
import time
from typing import Dict, List
from pydantic import BaseModel
from starlette.websockets import WebSocket

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class DeviceInfo(BaseModel):
    """Chatpool device metadata.
    """

    device_id: str
    connected_at: float
    message_count: int


class Pool:
    """Pool state, comprising connected devices.
    """

    def __init__(self):
        log.info("Creating new empty pool")
        self._devices: Dict[str, WebSocket] = {}
        self._device_meta: Dict[str, DeviceInfo] = {}

    def __len__(self) -> int:
        """Get the number of devices in the pool.
        """
        return len(self._devices)

    @property
    def empty(self) -> bool:
        """Check if the pool is empty.
        """
        return len(self._devices) == 0

    @property
    def device_list(self) -> List[str]:
        """Return a list of IDs for connected devices.
        """
        return list(self._devices)

    def add_device(self, device_id: str, websocket: WebSocket):
        """Add a device websocket, keyed by corresponding device ID.

        Raises:
            ValueError: If the `device_id` already exists within the pool.
        """
        if device_id in self._devices:
            raise ValueError(f"Device {device_id} is already in the pool")
        log.info("Adding device %s to pool", device_id)
        self._devices[device_id] = websocket
        self._device_meta[device_id] = DeviceInfo(
            device_id=device_id, connected_at=time.time(), message_count=0
        )

    async def remove_device(self, device_id: str):
        """Forcibly disconnect a device from the pool.

        We do not need to call `remove_device`, as this will be invoked automatically
        when the websocket connection is closed by the `PoolLive.on_disconnect` method.

        Raises:
            ValueError: If the `device_id` is not held within the pool.
        """
        if device_id not in self._devices:
            raise ValueError(f"Device {device_id} is not in the pool")
        await self._devices[device_id].send_json(
            {
                "type": "POOL_REMOVE",
                "data": {"msg": "You have been removed from the Devicepool!"},
            }
        )
        log.info("Removing device %s from pool", device_id)
        await self._devices[device_id].close()

    def remove_device(self, device_id: str):
        """Remove a device from the pool.

        Raises:
            ValueError: If the `device_id` is not held within the pool.
        """
        if device_id not in self._devices:
            raise ValueError(f"Device {device_id} is not in the pool")
        log.info("Removing device %s from pool", device_id)
        del self._devices[device_id]
        del self._device_meta[device_id]

    def get_device(self, device_id: str) -> DeviceInfo | None:
        """Get metadata on a device.
        """
        return self._device_meta.get(device_id)

    async def whisper(self, from_device: str, to_device: str, msg: str):
        """Send a private message from one device to another.

        Raises:
            ValueError: If either `from_device` or `to_device` are not present
                within the pool.
        """
        if from_device not in self._devices:
            raise ValueError(f"Calling device {from_device} is not in the pool")
        log.info("Device %s messaging device %s -> %s", from_device, to_device, msg)
        if to_device not in self._devices:
            await self._devices[from_device].send_json(
                {
                    "type": "ERROR",
                    "data": {"msg": f"Device {to_device} is not in the pool!"},
                }
            )
            return
        await self._devices[to_device].send_json(
            {
                "type": "WHISPER",
                "data": {"from_device": from_device, "to_device": to_device, "msg": msg},
            }
        )

    async def send_to_device(self, to_device_id: str, msg: str):
        """Send a private message server to device.

        Raises:
            ValueError: If either `to_device` are not present
                within the pool.
        """
        log.info("Messaging device %s -> %s", to_device_id, msg)
        if to_device_id not in self._devices:
            raise ValueError(f"Device {to_device_id} is not in the pool")
        await self._devices[to_device_id].send_json(
            {
                "type": "MESSAGE",
                "data": {"device_id": "to " + to_device_id + " from server", "msg": msg},
            }
        )

    async def broadcast_message(self, device_id: str, msg: str):
        """Broadcast message to all connected devices.
        """
        self._device_meta[device_id].message_count += 1
        for websocket in self._devices.values():
            await websocket.send_json(
                {"type": "MESSAGE", "data": {"device_id": device_id, "msg": msg}}
            )

    async def broadcast_device_joined(self, device_id: str):
        """Broadcast message to all connected devices.
        """
        for websocket in self._devices.values():
            await websocket.send_json({"type": "USER_JOIN", "data": device_id})

    async def broadcast_device_left(self, device_id: str):
        """Broadcast message to all connected devices.
        """
        for websocket in self._devices.values():
            await websocket.send_json({"type": "USER_LEAVE", "data": device_id})
