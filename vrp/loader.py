import asyncio
import re
from os import PathLike
from typing import Any, Callable, Dict

import aiofiles

from vrp.common.types.coordinate import Coordinate
from vrp.common.types.delivery_load import DeliveryLoad

regex_load_line = re.compile(
    "^(?P<load_number>[-\d\.]+)[,\s]+\(?(?P<pickup_latitude>(?:[\d\.-]+))[ ,]\(?(?P<pickup_longitude>(?:[\d\.-]+))\)?[,\s]+\(?(?P<dropoff_latitude>(?:[\d\.-]+))[ ,]\(?(?P<dropoff_longitude>(?:[\d\.-]+))\)[\s]*?"
)


def _parse_coordinate(coordinateString: str) -> Dict[str, float]:
    """
    Parses a coordinate string into a dictionary of it's consituant parts.

    Args:
        location (str): Latitude and Longitude separated by a ',' with or without being wrapped in parenthesis

    Returns:
        Dict[str, float]: Dictionary with 'latitude' and 'longitude' keys and float values
    """
    latitude, longitude = map(float, coordinateString.strip("()").split(","))
    return {"latitude": latitude, "longitude": longitude}


class FileLoader:

    def __init__(self, add_delivery_load: Callable[[DeliveryLoad], Any]) -> None:
        self.line_format = regex_load_line
        self._add_delivery_load = add_delivery_load

    async def _parse_line(self, line: str):
        """
        Parses a string representing a 'load' to be delivered.

        Args:
            lint (str): A string containing the loadNumber, and pickup/dropoff coordinates. Expected format `loadNumber (pickup_latitude,pickup_longitude) (dropoff_latitude,dropoff_longitude)
        """
        if line is None:
            return
        match = regex_load_line.match(line)
        if match is None:
            return
        pickup = Coordinate(
            latitude=float(match.group("pickup_latitude")),
            longitude=float(match.group("pickup_longitude")),
        )
        dropoff = Coordinate(
            latitude=float(match.group("dropoff_latitude")),
            longitude=float(match.group("dropoff_longitude")),
        )
        load_number = int(match.group("load_number"))
        self._add_delivery_load(
            DeliveryLoad(start=pickup, end=dropoff, load_number=load_number)
        )

    async def read(self, filePath: PathLike):
        async with aiofiles.open(filePath, "r") as file:
            file_tasks = []
            async for line in file:
                file_tasks.append(asyncio.create_task((self._parse_line(line))))

            await asyncio.gather(*file_tasks)
