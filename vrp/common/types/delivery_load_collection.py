from copy import deepcopy
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, cast

from vrp.common.types.coordinate import Coordinate
from vrp.common.types.coordinate_vector import CoordinateVector
from vrp.common.types.delivery_load import DeliveryLoad
from vrp.common.types.delivery_load_connection import DeliveryLoadConnection
from vrp.common.types.truck import Truck

ConnectionSelector = Callable[
    [Truck, List[DeliveryLoadConnection]], DeliveryLoadConnection
]


def connection_visited_condition(
    connection: DeliveryLoadConnection, is_unvisited: Optional[bool]
) -> bool:
    if is_unvisited is None or not isinstance(connection.end, DeliveryLoad):
        return True
    return (
        connection.end.visited_by is None
        if is_unvisited
        else connection.end.visited_by is not None
    )


@dataclass(frozen=True)
class DeliveryLoadCollection:
    _connections: Dict[
        DeliveryLoad | Coordinate | CoordinateVector, List[DeliveryLoadConnection]
    ] = field(init=False, repr=False, default={})
    _origin: Coordinate = field(init=False, repr=False, default=Coordinate(0.0, 0.0))
    _delivery_loads: List[DeliveryLoad] = field(init=False, repr=False, default=[])

    def __post_init__(self):
        object.__setattr__(self, "_origin", Coordinate(0, 0))
        object.__setattr__(self, "_delivery_loads", [])
        self.add(self._origin)

    @property
    def origin(self) -> List[DeliveryLoadConnection]:
        return self._connections[self._origin]

    @property
    def all_nodes_complete(self) -> bool:
        return (
            len([load for load in self._delivery_loads if load.visited_by is not None])
            == 0
        )

    def connections_for(
        self,
        node: DeliveryLoad | CoordinateVector | Coordinate,
        unvisited: Optional[bool] = None,
    ) -> List[DeliveryLoadConnection]:
        return [
            connection
            for connection in self._connections[node]
            if connection_visited_condition(connection, unvisited)
        ]

    def add(
        self, delivery_load: DeliveryLoad | Coordinate | CoordinateVector
    ) -> List[DeliveryLoadConnection]:
        new_delivery_load = deepcopy(delivery_load)
        self._connections[new_delivery_load] = []
        for delivery in self._connections.keys():
            self._connections[delivery].append(
                DeliveryLoadConnection(delivery, new_delivery_load)
            )
            self._connections[delivery_load].append(
                DeliveryLoadConnection(new_delivery_load, delivery)
            )
        if isinstance(delivery_load, DeliveryLoad):
            self._delivery_loads.append(cast(DeliveryLoad, new_delivery_load))
        return self._connections[new_delivery_load]
