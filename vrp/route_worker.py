from copy import deepcopy
import gevent
import gevent.pool
from vrp.const import ORIGIN_INDEX
from vrp.strategies.base_strategy import BaseRoutingStrategy
import pandas as pd


from typing import List, Optional, Sequence, Set

from .common import Truck, chunk_array, flatten_array


class RouteWorker:

    def __init__(
        self,
        max_distance: float,
        load_distances: pd.DataFrame,
        strategy: BaseRoutingStrategy,
    ):
        self.load_distances = load_distances
        self.routing_strategy = strategy
        self.max_distance = max_distance

    def find_optimal_routes(self) -> Sequence[gevent.Greenlet]:
        """
        Finds the routes that complete all loads following the given strategy

        Returns:
            List[List[int]]: List containing the list the load numbers a driver/truck needs to follow to complete the load set.
        """

        def trucks_under_maximum(trucks: List[Truck]) -> bool:
            return (
                len(
                    [
                        truck
                        for truck in trucks
                        if truck.distance_travelled > self.max_distance
                    ]
                )
                == 0
            )

        all_loads = set(self.load_distances.index.astype(int))
        all_loads.remove(ORIGIN_INDEX)

        def process(truck_count: int, pending_loads: Set[int]) -> Optional[List[Truck]]:
            trucks = self._find_routes(truck_count, pending_loads)
            if (
                trucks is not None
                and len(pending_loads) == 0
                and trucks_under_maximum(trucks)
            ):
                return trucks

            return None

        def process_pool(truck_counts: List[int]) -> List[gevent.Greenlet]:
            pool = gevent.pool.Pool(len(truck_counts))
            greenlets = [
                pool.spawn(process, truck_count, deepcopy(all_loads))
                for truck_count in truck_counts
            ]
            return greenlets

        greenlets = [
            process_pool(list(chunk))
            for chunk in chunk_array(range(1, len(all_loads)), 100)
        ]

        return flatten_array(greenlets)

    def _find_routes(
        self, truck_count: int, pending_loads: Set[int]
    ) -> Optional[List[Truck]]:
        """
        Attempts to find routes that complete all loads using the number of trucks provided.

        Args:
            truck_count (int): Number of trucks to perform routes
        """
        trucks = [Truck() for i in range(0, truck_count)]

        def finish_truck(truck: Truck):
            truck.distance_travelled += self.routing_strategy.distance_to_origin(
                self.load_distances, truck.current_index
            )
            truck.current_index = ORIGIN_INDEX
            truck.finished = True

        def get_unfinished_trucks() -> List[Truck]:
            return [truck for truck in trucks if not truck.finished]

        while len(pending_loads) > 0:
            unfinished_trucks = get_unfinished_trucks()
            if len(unfinished_trucks) != truck_count:
                break
            for truck in get_unfinished_trucks():
                next_load = None
                if len(pending_loads) > 0:
                    next_load = self.routing_strategy.get_next_load_index(
                        self.load_distances,
                        pending_loads,
                        truck.distance_travelled,
                        truck.current_index,
                    )
                if next_load is None or next_load.load_index is None:
                    finish_truck(truck)
                    continue

                truck.distance_travelled += (
                    next_load.distance_to_pickup + next_load.distance_to_dropoff
                )
                truck.current_index = next_load.load_index
                truck.route.append(next_load.load_index)
                pending_loads.remove(next_load.load_index)

        for truck in trucks:
            finish_truck(truck)

        return trucks if len(pending_loads) == 0 else None
