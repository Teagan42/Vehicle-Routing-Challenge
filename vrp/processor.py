from typing import List, cast
import pandas as pd
from scipy.spatial import distance_matrix

from vrp.const import MAX_FLOAT
from .strategies import routing_strategies
from .route_worker import RouteWorker
from .common import (
    LoadCoordinateTables,
    LoadCoordinatesTable,
    LoadDeliveryData,
    Truck,
    calculate_cost,
)


class RouteProcessor:
    """
    Determines routes that complete each load in the data set.
    """

    def __init__(
        self, delivery_data: List[LoadDeliveryData], max_distance: float = 12 * 60
    ):
        loadDataTables = self._build_data_tables((delivery_data))
        self.load_distances: pd.DataFrame = pd.DataFrame(
            distance_matrix(
                loadDataTables.dropoff_data_frame[["latitude", "longitude"]],
                loadDataTables.pickup_data_frame[["latitude", "longitude"]],
            ),
            index=loadDataTables.dropoff_data_frame["load_number"],
            columns=loadDataTables.dropoff_data_frame["load_number"],
        )
        self.max_distance = max_distance

    def _build_data_tables(
        self, delivery_data: List[LoadDeliveryData]
    ) -> LoadCoordinateTables:
        """
        Creates the data tables used to calculate route distances.

        Args:
            delivery_data (List[LoadDeliveryData]): List of delivery load data items.

        Returns:
            LoadCoordinateTables: A structure containing pickup and drop off tables.
        """
        pickup_locations: LoadCoordinatesTable = LoadCoordinatesTable(
            {
                "load_number": [item.load_number for item in delivery_data],
                "latitude": [item.pickup.latitude for item in delivery_data],
                "longitude": [item.pickup.longitude for item in delivery_data],
            }
        )
        dropoff_locations: LoadCoordinatesTable = LoadCoordinatesTable(
            {
                "load_number": [item.load_number for item in delivery_data],
                "latitude": [item.dropoff.latitude for item in delivery_data],
                "longitude": [item.dropoff.longitude for item in delivery_data],
            }
        )

        return LoadCoordinateTables(
            pickup_data_frame=pd.DataFrame(pickup_locations),
            dropoff_data_frame=pd.DataFrame(dropoff_locations),
        )

    def run(self):
        greenlets = [
            RouteWorker(
                self.max_distance,
                self.load_distances,
                strategy_cls(),
            ).find_optimal_routes()
            for strategy_cls in routing_strategies
        ]

        # gevent.joinall(greenlets)

        cheapest: List[Truck] = []
        cost: float = MAX_FLOAT

        for results in [g for g in greenlets if g is not None]:
            trucks = cast(List[Truck], results)
            total_cost = calculate_cost(trucks)

            if total_cost < cost:
                cheapest = trucks

        for truck in cheapest:
            print(truck.route)
