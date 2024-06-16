from dataclasses import dataclass, field

from vrp.common.calculations import euclidean_distance


@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float
    distance_from_origin: float = field(init=False, repr=True)

    def __post_init__(self):
        if self.latitude == 0 and self.longitude == 0:
            distance = 0.0
        else:
            distance = euclidean_distance(self, Coordinate(0, 0))

        object.__setattr__(self, "distance_from_origin", distance)
