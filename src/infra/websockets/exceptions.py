from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class WebSocketIsNotConnectException(ApplicationException):
    @property
    def message(self):
        return "WebSocket is not connected."
