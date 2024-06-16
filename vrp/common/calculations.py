from typing import List

from numpy import sqrt

from vrp.common.types.coordinate import Coordinate
from vrp.common.types.coordinate_vector import CoordinateVector


def euclidean_distance(a: Coordinate, b: Coordinate) -> float:
    """
    Calculate the Euclidean distance between two locations.
    """
    return sqrt((a.latitude - b.latitude) ** 2 + (a.longitude - b.longitude) ** 2)


def route_distance(route_segments: List[CoordinateVector]) -> float:
    """
    Calculate the route's total distance across all segments.

    Args:
        route_segments The segments that constitute a route.

    Returns:
        float: The sum of Euclidean distances between each coordinate on the route
    """
    return sum([segment.distance for segment in route_segments])
