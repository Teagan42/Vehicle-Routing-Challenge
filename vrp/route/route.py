from typing import List, NamedTuple

from vrp.load.load import Load


class Route(NamedTuple):
    """
    A sequence of loads with the total distance travelled over this route.
    """

    # The stops, in sequential order, that make up the route.
    loads: List[Load]
    # The total distance the route covers.
    distance: float
