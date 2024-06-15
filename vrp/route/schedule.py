from typing import List, NamedTuple

from vrp.route.route import Route


class schedule(NamedTuple):
    """
    The list of routes that completes all loads with the associated cost and distance.
    """

    # The routes for each truck
    routes: List[Route]
    # The cost for all necessary trucks to complete their assigned route.
    cost: float
    # The total distance travelled by all trucks.
    distance: float
