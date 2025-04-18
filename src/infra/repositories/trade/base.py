from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.trade import TradeEntity


@dataclass
class BaseTradeRepository(ABC):
    @abstractmethod
    async def save_trade(self, trade: TradeEntity): ...

    @abstractmethod
    async def delete_old_trades(self): ...
