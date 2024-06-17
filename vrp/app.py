from gevent import monkey

from .loader import FileLoader
from .processor import RouteProcessor

monkey.patch_all()


class App:

    def __init__(self) -> None:
        self.file_loader = FileLoader()

    async def run(self, file_path: str):
        delivery_data = await self.file_loader.read_load_file(file_path)

        RouteProcessor(delivery_data).run()
