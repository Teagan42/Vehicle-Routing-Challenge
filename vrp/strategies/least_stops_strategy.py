from typing import Dict, Optional, Set

import pandas as pd

from vrp.const import MAX_FLOAT
from vrp.strategies.base_strategy import BaseRoutingStrategy, NextRouteLoad


class LeastStopsRoutingStrategy(BaseRoutingStrategy):
    def get_next_load_index(
        self,
        load_distances: pd.DataFrame,
        loads_pending: Set[int],
        distance_travelled: float,
        current_load_index: int,
    ) -> Optional[NextRouteLoad]:
        """
        Gets the longest and furthest load number from the current load.

        Args:
            load_distances (pd.DataFrame): Distance matrix
            loads_pending (List[int]): Loads yet to be completed
            distance_travelled (float): Distance already travelled
            current_load_index (int): The current load number

        Returns:
            int: The load number of the job furthest from the current node taking the most time to complete
        """
        route_loads: Dict[int, Optional[NextRouteLoad]] = {}

        def calculate_distance(load_number: int) -> float:
            if (
                self.get_total_distance(load_distances, current_load_index, load_number)
                + distance_travelled
                > self.max_distance
            ):
                route_loads[load_number] = None
                return -MAX_FLOAT
            next_load = NextRouteLoad(
                load_index=load_number,
                distance_to_dropoff=self.get_load_distance(load_distances, load_number),
                distance_to_pickup=self.get_distance(
                    load_distances, current_load_index, load_number
                ),
            )
            route_loads[load_number] = next_load
            return next_load.distance_to_pickup + next_load.distance_to_dropoff

        load_index = max(loads_pending, key=calculate_distance)
        return route_loads[load_index]
