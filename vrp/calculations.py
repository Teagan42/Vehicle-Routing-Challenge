from math import sqrt

from vrp.load.location import Location


def cartesian_distance(a: Location, b: Location) -> float:
    return sqrt((a.latitude - b.latitude) ** 2 + (a.longitude - b.longitude) ** 2)
