from typing import List

from vrp.common.calculations import euclidean_distance
from vrp.common.types.coordinate import Coordinate
from vrp.common.types.delivery_load import DeliveryLoad
from vrp.common.types.delivery_load_connection import DeliveryLoadConnection


class Truck:
    def __init__(
        self,
        id: int,
        max_distance: int,
        location: Coordinate,
    ) -> None:
        self._max_distance = max_distance
        self.id = id
        self.location: Coordinate = location
        self.distance_travelled = 0
        self.route: List[DeliveryLoad] = []

    @property
    def is_at_origin(self) -> bool:
        if not isinstance(self.location, Coordinate):
            return False
        return self.location.latitude == 0 and self.location.longitude == 0

    def step(self, connection: DeliveryLoadConnection) -> bool:
        if isinstance(connection.start, De)
        distance = euclidean_distance(self.location, connection.start)
        if self.distance_travelled + connection.distance > self._max_distance:
            return False

        self.location = connection.traverse(self.id)
        if isinstance(self.location, DeliveryLoad):
            self.route.append(self.location)

        return True
