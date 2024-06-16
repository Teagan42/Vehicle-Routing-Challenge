from typing import List

from vrp.common.types.delivery_load_collection import (
    ConnectionSelector,
    DeliveryLoadCollection,
)
from vrp.common.types.truck import Truck


class RouteTaskWorker:
    def __init__(
        self,
        delivery_loads: DeliveryLoadCollection,
        connection_selector: ConnectionSelector,
        max_distance: int = 12 * 60,
    ) -> None:
        self._trucks = [
            Truck(index, self._max_distance, connection.start)
            for index, connection in enumerate(self._delivery_loads.origin)
        ]
        self._delivery_loads: DeliveryLoadCollection = delivery_loads
        self._max_distance = max_distance
        self._connection_selector = connection_selector

    @property
    def all_trucks_at_origin(self) -> bool:
        return len([truck.is_at_origin is not True for truck in self._trucks]) == 0

    def run(self) -> List[Truck]:
        while not self._delivery_loads.all_nodes_complete:
            for truck in self._trucks:
                location = truck.location
                connection = self._connection_selector(
                    self._delivery_loads.connections_for(location, unvisited=True)
                )
                truck.step(connection)
        return self._trucks
