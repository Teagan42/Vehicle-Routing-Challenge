from typing import NamedTuple


class Location(NamedTuple):
    """
    Defines a point on a delivery route.
    """

    # The latitude of the location
    latitude: float
    # The longitude of the location
    longitude: float
