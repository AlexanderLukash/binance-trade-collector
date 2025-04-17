from functools import lru_cache

from punq import Container, Scope

from src.infra.filesystem.base import BaseAssetsProviders
from src.infra.filesystem.file_assets import FileAssetProvider
from src.infra.websockets.managers import BaseConnectionManager, ConnectionManager
from src.settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def init_connection_manager() -> BaseConnectionManager:
        return ConnectionManager(
            _uri=config.binance_websockets_url,
        )

    container.register(
        BaseConnectionManager,
        factory=init_connection_manager,
        scope=Scope.singleton,
    )

    def init_assets_provider() -> BaseAssetsProviders:
        return FileAssetProvider(
            _filepath=config.path_to_assets,
        )

    container.register(
        BaseAssetsProviders,
        factory=init_assets_provider,
        scope=Scope.singleton,
    )

    return container
