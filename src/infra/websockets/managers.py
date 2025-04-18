import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import websockets
from websockets.legacy.client import WebSocketClientProtocol

from src.infra.websockets.exceptions import WebSocketIsNotConnectException


@dataclass
class BaseConnectionManager(ABC):
    _uri: str

    @abstractmethod
    async def connect(self): ...

    @abstractmethod
    async def send_json(self, message: dict): ...

    @abstractmethod
    async def receive_json(self) -> dict: ...


@dataclass
class ConnectionManager(BaseConnectionManager):
    _connection: Optional[WebSocketClientProtocol] = None

    async def connect(self):
        self._connection = await websockets.connect(self._uri)  # noqa

    async def send_json(self, message: dict):
        if not self._connection:
            raise WebSocketIsNotConnectException()
        await self._connection.send(json.dumps(message))

    async def receive_json(self) -> dict:
        if not self._connection:
            raise WebSocketIsNotConnectException()
        raw_message = await self._connection.recv()
        return json.loads(raw_message)
