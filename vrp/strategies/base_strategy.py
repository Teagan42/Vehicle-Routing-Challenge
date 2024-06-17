import abc
from typing import NamedTuple, Set, Optional

import numpy as np
import pandas as pd

from vrp.const import ORIGIN_INDEX


class NextRouteLoad(NamedTuple):
    load_index: int
    distance_to_pickup: float
    distance_to_dropoff: float


class BaseRoutingStrategy(abc.ABC):

    def __init__(self, max_distance: float = 12 * 60) -> None:
        self.max_distance = max_distance

    def to_float(
        self,
        load_distances: pd.DataFrame,
        current_load_number: int,
        next_load_number: int,
    ) -> float:
        """
        Converts a DataFrame cell to a 32bit float.

        Args:
            current_load_number (int): The current load identifier.
            next_load_number (int): The identifier of the possible next load.

        Returns:
            np.float32: The distance from the matrix as a 32-bit float.
        """
        return float(
            np.float32(
                "{:15f}".format(
                    load_distances.loc[current_load_number, next_load_number]
                )
            )
        )

    def get_next_load_index(self, load_distances: pd.DataFrame, loads_pending: Set[int], distance_travelled: float, current_load_index: int) -> Optional[NextRouteLoad]:  # type: ignore
        pass

    def get_distance(
        self, load_distances: pd.DataFrame, index_a: int, index_b: int
    ) -> float:
        """
        Gets the distance between two indicies.

        Args:
            load_distances (pd.DataFrame): Distance matrix
            index_a (int): Starting index
            index_b (int): Ending index

        Returns:
            float: The distance between a and b
        """
        return self.to_float(load_distances, index_a, index_b)

    def get_load_distance(self, load_distances: pd.DataFrame, load_index: int) -> float:
        """
        Each load has a defined start and end, and must be included in the calculation

        Args:
            load_distances (pd.DataFrame): Distance Matrix
            load_index (int): The load number to get the distance for

        Returns:
            float: The distance travelled completing the load
        """
        return self.get_distance(load_distances, load_index, load_index)

    def distance_to_origin(
        self, load_distances: pd.DataFrame, load_index: int
    ) -> float:
        """
        Gets the distance from the dropoff location and the origin

        Args:
            load_distances (pd.DataFrame): Distance matrix
            load_index (int): The load number to get the distance to the origin

        Returns:
            float: The distance travelled to get to the origin
        """
        return self.get_distance(load_distances, load_index, ORIGIN_INDEX)

    def get_total_distance(
        self, load_distances: pd.DataFrame, index_a: int, index_b: int
    ) -> float:
        """
        Gets the total distance to complete the next load

        Args:
            load_distances (pd.DataFrame): Distance matrix
            index_a (int): The current location
            index_b (int): The load number of the next load

        Returns:
            float: The sum of the distance to the pickup, drop off and then to the origin
        """
        if index_b == ORIGIN_INDEX:
            return self.distance_to_origin(load_distances, index_a)
        return (
            self.get_distance(load_distances, index_a, index_b)
            + self.get_load_distance(load_distances, index_b)
            + self.distance_to_origin(load_distances, index_b)
        )
