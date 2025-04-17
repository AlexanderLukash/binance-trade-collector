from dataclasses import dataclass

from src.infra.filesystem.base import BaseAssetsProviders


@dataclass()
class FileAssetProvider(BaseAssetsProviders):
    def get_asset_pairs(self) -> list[str]:
        with open(self._filepath, encoding="utf-8") as f:
            lines = f.readlines()
        return [
            line.strip().replace("/", "").lower() + "@trade"
            for line in lines
            if line.strip()
        ]
