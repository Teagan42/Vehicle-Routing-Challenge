from dataclasses import dataclass, field

from vrp.common.calculations import euclidean_distance
from vrp.common.types.coordinate import Coordinate


@dataclass(frozen=True)
class CoordinateVector:
    start: Coordinate
    end: Coordinate
    distance: float = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "distance", euclidean_distance(self.start, self.end))
