import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from tortoise import Tortoise
from tortoise.models import Model
from abc import ABC
from typing import Type

from src.domain.entities.trade import TradeEntity
from src.infra.repositories.trade.base import BaseTradeRepository
from src.infra.repositories.trade.models.trade import TradeModel
from src.infra.repositories.trade.models.trade_stat import TradeStatModel

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

    async def save_trade_batch(self, trades: list[TradeEntity]):
        await TradeModel.bulk_create(
            [
                TradeModel(
                    oid=trade.oid,
                    symbol=trade.symbol,
                    trade_id=trade.trade_id,
                    price=trade.price,
                    quantity=trade.quantity,
                    is_buyer_market_maker=trade.is_buyer_market_maker,
                    created_at=trade.created_at,
                )
                for trade in trades
            ],
        )
        logger.info(
            f"Saved {len(trades)} trades.",
        )

    async def update_or_save_trade(self, trade: TradeEntity):
        await TradeModel.update_or_create(
            defaults={
                "trade_id": trade.trade_id,
                "price": trade.price,
                "quantity": trade.quantity,
                "is_buyer_market_maker": trade.is_buyer_market_maker,
                "created_at": trade.created_at,
            },
            symbol=trade.symbol,
        )
        logger.info(f"Trade for {trade.symbol} updated or created.")

    async def update_stat(self, trade: TradeEntity):
        stat = await TradeStatModel.filter(symbol=trade.symbol).first()
        now = datetime.now(timezone.utc)

        if not stat:
            await TradeStatModel.create(
                symbol=trade.symbol,
                min_price=trade.price,
                max_price=trade.price,
                avg_price=trade.price,
                trades_count=1,
                last_updated=now,
                stat_reset_time=now,
            )
        else:
            if now - stat.stat_reset_time > timedelta(hours=24):
                stat.min_price = trade.price
                stat.max_price = trade.price
                stat.avg_price = trade.price
                stat.trades_count = 1
                stat.stat_reset_time = now
            else:
                stat.min_price = min(stat.min_price, trade.price)
                stat.max_price = max(stat.max_price, trade.price)
                stat.avg_price = round(
                    (stat.avg_price * stat.trades_count + trade.price)
                    / (stat.trades_count + 1),
                    5,
                )
                stat.trades_count += 1

            stat.last_updated = now
            await stat.save()

        logger.info(f"Updated stats for {trade.symbol}")
