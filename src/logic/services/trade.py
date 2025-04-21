from dataclasses import dataclass

from src.domain.entities.trade import TradeEntity
from src.infra.repositories.trade.base import BaseTradeRepository
from src.logic.services.base import BaseTradeService


@dataclass
class ORMTradeService(BaseTradeService):
    trade_repo: BaseTradeRepository

    async def create_trade(self, trade: TradeEntity):
        await self.trade_repo.save_trade(trade=trade)

    async def delete_old_trades(self):
        await self.trade_repo.delete_old_trades()

    async def create_trade_batch(self, trades: list[TradeEntity]):
        await self.trade_repo.save_trade_batch(trades=trades)

    async def update_or_create_trade(self, trade: TradeEntity):
        await self.trade_repo.update_or_save_trade(trade=trade)

    async def update_stat_by_trade(self, trade: TradeEntity):
        await self.trade_repo.update_stat(trade=trade)
