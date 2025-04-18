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
