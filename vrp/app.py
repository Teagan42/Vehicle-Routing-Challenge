from pathlib import Path

from vrp.common.types.delivery_load_collection import DeliveryLoadCollection
from vrp.loader import FileLoader


class App:
    def __init__(self):
        self._delivery_loads = DeliveryLoadCollection()
        self._file_loader = FileLoader(self._delivery_loads.add)

    async def run(self, file_path: str):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"{file_path} was not found on the system.")
        await self._file_loader.read(path)
