from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.trade import TradeEntity


@dataclass
class BaseTradeService(ABC):
    @abstractmethod
    async def create_trade(self, trade: TradeEntity): ...

    @abstractmethod
    async def delete_old_trades(self): ...
