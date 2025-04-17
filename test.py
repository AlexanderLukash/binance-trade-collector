# import asyncio
# import json
# import websockets
#
# # Читаем валютные пары из файла и готовим список параметров для подписки
# def load_asset_pairs(filename="assets.txt"):
#     with open(filename, "r") as f:
#         lines = f.readlines()
#     pairs = [line.strip().replace("/", "").lower() + "@trade" for line in lines if line.strip()]
#     return pairs
#
# # Подключение к Binance WebSocket и подписка
# async def binance_trade_subscribe():
#     url = "wss://stream.binance.com:9443/ws"
#     params = load_asset_pairs()
#     subscribe_msg = {
#         "method": "SUBSCRIBE",
#         "params": params,
#         "id": 1
#     }
#
#     async with websockets.connect(url) as websocket:
#         await websocket.send(json.dumps(subscribe_msg))
#         print(f"Subscribed to {len(params)} trade streams.")
#
#         while True:
#             response = await websocket.recv()
#             data = json.loads(response)
#             print(data)  # В реальной ситуации — логгировать или обрабатывать
#
# # Запуск
# # asyncio.run(binance_trade_subscribe())  # Это закомментировано, так как мы не запускаем здесь
#
# load_asset_pairs()[:5]  # Покажем первые 5 пар для проверки

from punq import Container

from src.infra.filesystem.base import BaseAssetsProviders
from src.logic.init import init_container


# async def run():
#     container: Container = init_container()
#     client = container.resolve(BaseConnectionManager)
#     await client.connect()
#
#     await client.send_json({
#         "method": "SUBSCRIBE",
#         "params": ["btcusdt@trade"],
#         "id": 1
#     })
#
#     while True:
#         data = await client.receive_json()
#         print(data)
#
# asyncio.run(run())


if __name__ == "__main__":
    container: Container = init_container()
    provider = container.resolve(BaseAssetsProviders)
    print(len(provider.get_asset_pairs()))
