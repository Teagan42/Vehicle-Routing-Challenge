from typing import NamedTuple

from vrp.load.location import Location


class Load(NamedTuple):
    """
    Defines the location this load is picked up and the location where it is to be dropped off.
    """

    # The identifier for this load
    load_number: int
    # The location the load is picked up
    pickup: Location
    # The location the load is dropped off
    dropoff: Location
    # The distance between the pickup and dropoff locations
    distance: float
