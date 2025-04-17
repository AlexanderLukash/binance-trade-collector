import asyncio
import logging

from punq import Container

from src.domain.converters.trade import convert_data_to_entity
from src.infra.filesystem.base import BaseAssetsProviders
from src.infra.repositories.trade.base import BaseTradeRepository
from src.infra.websockets.managers import BaseConnectionManager
from src.logic.init import init_container
from src.logic.services.base import BaseTradeService
from src.logic.services.shudeler import start_scheduler
from src.settings.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
container: Container = init_container()


async def binance_trade_subscribe():
    tortoise_db: BaseTradeRepository = container.resolve(BaseTradeRepository)
    await tortoise_db._init_db()
    assets_provider: BaseAssetsProviders = container.resolve(BaseAssetsProviders)
    websocket_client: BaseConnectionManager = container.resolve(BaseConnectionManager)
    trade_service: BaseTradeService = container.resolve(BaseTradeService)
    params = assets_provider.get_asset_pairs()
    await websocket_client.connect()

    await websocket_client.send_json(
        message={
            "method": "SUBSCRIBE",
            "params": params,
            "id": 1,
        },
    )

    logger.info(f"Subscribed to {len(params)} trade streams.")
    await trade_service.delete_old_trades()
    await start_scheduler()

    while True:
        data = await websocket_client.receive_json()
        if data.get("e") == "trade":
            trade = convert_data_to_entity(data)
            await trade_service.create_trade(
                trade=trade,
            )


asyncio.run(binance_trade_subscribe())
