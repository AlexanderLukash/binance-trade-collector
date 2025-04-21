from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.domain.entities.trade import TradeEntity


@dataclass
class BaseTradeService(ABC):
    @abstractmethod
    async def create_trade(self, trade: TradeEntity): ...

    @abstractmethod
    async def delete_old_trades(self): ...

    @abstractmethod
    async def create_trade_batch(self, trades: list[TradeEntity]): ...

    @abstractmethod
    async def update_or_create_trade(self, trade: TradeEntity): ...

    @abstractmethod
    async def update_stat_by_trade(self, trade: TradeEntity): ...
