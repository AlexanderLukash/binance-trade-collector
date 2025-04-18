from functools import lru_cache

from punq import Container, Scope

from src.infra.filesystem.base import BaseAssetsProviders
from src.infra.filesystem.file_assets import FileAssetProvider
from src.infra.repositories.trade.base import BaseTradeRepository
from src.infra.repositories.trade.models.trade import TradeModel
from src.infra.repositories.trade.postgresql import TradePostgresRepository
from src.infra.websockets.managers import BaseConnectionManager, ConnectionManager
from src.logic.services.base import BaseTradeService
from src.logic.services.trade import ORMTradeService
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

    def init_trade_repo() -> BaseTradeRepository:
        return TradePostgresRepository(
            _db_url=config.database_url,
            models=[TradeModel],
        )

    container.register(
        BaseTradeRepository,
        factory=init_trade_repo,
        scope=Scope.singleton,
    )

    def init_trade_service() -> BaseTradeService:
        trade_repo = container.resolve(BaseTradeRepository)
        return ORMTradeService(trade_repo=trade_repo)

    container.register(
        BaseTradeService,
        factory=init_trade_service,
        scope=Scope.singleton,
    )

    return container
