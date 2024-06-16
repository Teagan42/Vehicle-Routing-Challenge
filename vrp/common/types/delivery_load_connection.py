from dataclasses import dataclass, field

from vrp.common.calculations import euclidean_distance
from vrp.common.types.coordinate import Coordinate
from vrp.common.types.coordinate_vector import CoordinateVector
from vrp.common.types.delivery_load import DeliveryLoad


@dataclass(frozen=True)
class DeliveryLoadConnection:
    start: DeliveryLoad | CoordinateVector | Coordinate
    end: DeliveryLoad | CoordinateVector | Coordinate
    distance: float = field(init=False, repr=True)

    def __post_init__(self):
        if isinstance(self.start, CoordinateVector):
            start = self.start.end
        else:
            start = self.start

        if isinstance(self.end, CoordinateVector):
            end = self.end.start
        else:
            end = self.end

        object.__setattr__(self, "distance", euclidean_distance(end, start))

    def traverse(self, by: int) -> "DeliveryLoad | CoordinateVector | Coordinate":
        if isinstance(self.end, DeliveryLoad):
            return self.end.visit(by)
        return self.end
