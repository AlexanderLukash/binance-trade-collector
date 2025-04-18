import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from tortoise import Tortoise
from tortoise.models import Model
from abc import ABC
from typing import Type

from src.domain.entities.trade import TradeEntity
from src.infra.repositories.trade.base import BaseTradeRepository
from src.infra.repositories.trade.models.trade import TradeModel

logger = logging.getLogger(__name__)


@dataclass
class BasePostgresRepository(ABC):
    _db_url: str
    models: list[Type[Model]]

    async def _init_db(self):
        logger.info("Start initialize database")
        await Tortoise.init(
            db_url=self._db_url,
            modules={"models": [model.__module__ for model in self.models]},
        )
        await Tortoise.generate_schemas()
        logger.info("Database was init and schemas created.")

    @staticmethod
    async def close_db():
        await Tortoise.close_connections()

    @staticmethod
    async def get_model(model_class: Type[Model]) -> list[Model]:
        return await model_class.all()


@dataclass
class TradePostgresRepository(BaseTradeRepository, BasePostgresRepository):
    async def save_trade(self, trade: TradeEntity):
        await TradeModel.create(
            oid=trade.oid,
            symbol=trade.symbol,
            trade_id=trade.trade_id,
            price=trade.price,
            quantity=trade.quantity,
            is_buyer_market_maker=trade.is_buyer_market_maker,
            created_at=trade.created_at,
        )
        logger.info(f"Trade {trade.trade_id} saved for {trade.symbol}")

    async def delete_old_trades(self):
        cutoff_date = datetime.now() - timedelta(days=2)
        deleted_count = await TradeModel.filter(created_at__lt=cutoff_date).delete()
        logger.info(
            f"Deleted {deleted_count} old trades older than {cutoff_date.isoformat()}",
        )
