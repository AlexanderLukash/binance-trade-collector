import asyncio
import logging
from collections import deque

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

    trade_buffer = deque(maxlen=1000)

    async def connect_and_subscribe():
        await websocket_client.connect()
        await websocket_client.send_json(
            message={
                "method": "SUBSCRIBE",
                "params": params,
                "id": 1,
            },
        )
        logger.info(f"Subscribed to {len(params)} trade streams.")

    async def save_trade_batch():
        while True:
            if trade_buffer:
                trades = list(trade_buffer)
                trade_buffer.clear()
                try:
                    await trade_service.create_trade_batch(trades)
                    logger.debug(f"Saved {len(trades)} trades to DB")
                except Exception as e:
                    logger.error(f"Failed to save trade batch: {e}")
            await asyncio.sleep(1)

    # Initial connection
    await connect_and_subscribe()
    await trade_service.delete_old_trades()
    await start_scheduler()

    asyncio.create_task(save_trade_batch())

    while True:
        try:
            data = await websocket_client.receive_json()
            if data.get("e") == "trade":
                trade = convert_data_to_entity(data)
                trade_buffer.append(trade)
        except Exception as e:
            logger.error(f"WebSocket connection closed: {e}. Reconnecting...")
            await connect_and_subscribe()


if __name__ == "__main__":
    asyncio.run(binance_trade_subscribe())
