from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseAssetsProviders(ABC):
    _filepath: str

    @abstractmethod
    def get_asset_pairs(self) -> list[str]:
        pass
