from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.trade import TradeEntity


@dataclass
class BaseTradeRepository(ABC):
    @abstractmethod
    async def save_trade(self, trade: TradeEntity): ...

    @abstractmethod
    async def delete_old_trades(self): ...

    @abstractmethod
    async def save_trade_batch(self, trades: list[TradeEntity]): ...

    @abstractmethod
    async def update_or_save_trade(self, trade: TradeEntity): ...

    @abstractmethod
    async def update_stat(self, trade: TradeEntity): ...
