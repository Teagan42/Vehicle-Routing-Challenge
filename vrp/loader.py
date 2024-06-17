from typing import List, Optional

import aiofiles


from .common import (
    Coordinate,
    LoadDeliveryData,
)


class FileLoader:
    """
    Reads and parses a file containing the load dataset.
    """

    def _parse_coordinate(self, coordinate_string: str) -> Coordinate:
        """
        Parses a coordinate string into a dictionary of it's consituant parts.

        Args:
            location (str): Latitude and Longitude separated by a ',' with or without being wrapped in parenthesis.

        Returns:
            Dict[str, float]: Dictionary with 'latitude' and 'longitude' keys and float values.
        """
        latitude, longitude = map(float, coordinate_string.strip("()\n").split(","))
        return Coordinate(latitude=latitude, longitude=longitude)

    def _parse_file_line(self, line: str) -> Optional[LoadDeliveryData]:
        """
        Parses a line in the load data file.

        Args:
            line (str): A string containing the load number and pickup/dropoff coordinates.

        Returns:
            Optional[LoadDeliveryData]: None if the string is a header, otherwise returns a typed structure representing the load for delivery.
        """
        if line.startswith("loadNumber"):
            return None

        tokens = line.split(" ")
        return LoadDeliveryData(
            load_number=int(tokens[0]),
            pickup=self._parse_coordinate(tokens[1]),
            dropoff=self._parse_coordinate(tokens[2]),
        )

    async def read_load_file(self, file_path: str) -> List[LoadDeliveryData]:
        """
        Reads in the specified file for delivery load information.

        Args:
            file_path (str): Path to the load data set file.

        Returns:
            List[LoadDeliveryData]: A list of load data structures.
        """
        rows: List[LoadDeliveryData] = [
            LoadDeliveryData(
                -1, Coordinate(0.0, 0.0), Coordinate(0.0, 0.0)
            )  # Append the origin to the list of rows
        ]

        async with aiofiles.open(file_path, "r") as f:
            async for line in f:
                row = self._parse_file_line(line)
                if row is not None:
                    rows.append(row)

        return rows
