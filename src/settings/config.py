from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    path_to_assets: str = Field(alias="PATH_TO_ASSETS", default="assets.txt")
    binance_websockets_url: str = Field(
        alias="BINANCE_WEBSOCKETS_URL",
        default="wss://stream.binance.com:9443/ws",
    )
