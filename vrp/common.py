from dataclasses import dataclass
import itertools
from typing import List, NamedTuple, Sequence, TypeVar, TypedDict

import pandas as pd


@dataclass()
class Coordinate:
    """
    Structure representing a position in space.
    """

    latitude: float
    longitude: float


@dataclass()
class LoadDeliveryData:
    """
    Parsed structure of a row in the load set file.
    """

    load_number: int
    pickup: Coordinate
    dropoff: Coordinate


class LoadCoordinatesTable(TypedDict):
    """
    Table representing a load and associated latitude and longitude values.
    """

    load_number: List[int]
    latitude: List[float]
    longitude: List[float]


class LoadCoordinateTables(NamedTuple):
    """
    Pickup and dropoff tables for the load data set.
    """

    pickup_data_frame: pd.DataFrame
    dropoff_data_frame: pd.DataFrame


class Truck:
    """Represents a truck traveling a route."""

    def __init__(self):
        self.route: List[int] = []
        self.distance_travelled: float = 0.0
        self.current_index: int = -1
        self.finished: bool = False


T = TypeVar("T")


def chunk_array(array: Sequence[T], chunk_size: int) -> Sequence[Sequence[T]]:
    return [array[i : i + chunk_size] for i in range(0, len(array), chunk_size)]


def flatten_array(array_of_arrays: Sequence[Sequence[T]]) -> Sequence[T]:
    return list(itertools.chain(*[item for item in array_of_arrays]))


def calculate_cost(trucks: List[Truck]) -> float:
    return 500 * len(trucks) + sum([truck.distance_travelled for truck in trucks])
