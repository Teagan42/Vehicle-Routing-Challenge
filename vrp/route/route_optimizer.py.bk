from typing import List

import pandas as pd

from vrp.route.routes import Routes
from vrp.route.truck import Truck


class RouteOptimizer:
    trucks: List[Truck]
    load_distances: pd.DataFrame
    price_per_truck: float
    price_per_distance: float
    minutes_passed: float

    def __init__(
        self,
        load_distances: pd.DataFrame,
        truck_count: int,
        price_per_truck: float = 1.0,
        price_per_distance: float = 1.0,
    ) -> None:
        self.trucks = [
            Truck(
                id=idx,
                distance_travelled=0.0,
                loads_completed=[],
                next_load=0,
                distance_to_next_load=0,
            )
            for idx in range(0, truck_count)
        ]
        self.load_distances = load_distances
        self.price_per_distance = price_per_distance
        self.price_per_truck = price_per_truck
        minutes_passed = 0

    def optmize(self) -> Routes:
        return Routes(routes=[], total_cost=0.0, total_distance=0.0)
    
    def _dispatch_truck(self, truck: Truck, load: int) -> None:
        
