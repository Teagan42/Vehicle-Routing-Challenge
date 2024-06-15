from typing import List, NamedTuple

from vrp.load.load import Load


class Route(NamedTuple):
    """
    Defines a driver's route as a sequence of stops.
    """

    driverId: int
    loads: List[Load]
