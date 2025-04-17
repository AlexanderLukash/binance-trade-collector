import asyncio
import logging


from src.domain.converters.trade import convert_data_to_entity
from src.infra.filesystem.base import BaseAssetsProviders
from src.infra.websockets.managers import BaseConnectionManager
from src.logic.init import init_container
from src.settings.logger import setup_logging

from punq import Container

setup_logging()
logger = logging.getLogger(__name__)
container: Container = init_container()


async def binance_trade_subscribe():
    assets_provider = container.resolve(BaseAssetsProviders)
    websocket_client = container.resolve(BaseConnectionManager)
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

    while True:
        data = await websocket_client.receive_json()
        if data.get("e") == "trade":
            trade = convert_data_to_entity(data)
            logger.info(trade)


asyncio.run(binance_trade_subscribe())
