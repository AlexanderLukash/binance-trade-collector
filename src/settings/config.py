from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    path_to_assets: str = Field(alias="PATH_TO_ASSETS", default="assets.txt")
    binance_websockets_url: str = Field(
        alias="BINANCE_WEBSOCKETS_URL",
        default="wss://stream.binance.com:9443/ws",
    )
    database_url: str = Field(
        alias="DATABASE_URL",
        default="postgres://my_user:my_password@localhost:5432/my_database",  # заміни на свій
    )
