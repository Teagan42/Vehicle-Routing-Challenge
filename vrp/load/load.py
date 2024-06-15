from typing import NamedTuple

from vrp.load.location import Location


class Load(NamedTuple):
    """
    Defines the locations a load must be picked up and where it must be dropped off.
    """

    id: int
    pickup: Location
    drop_off: Location
