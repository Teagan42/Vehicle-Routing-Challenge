from typing import Callable, Dict, List, Literal, Optional, Type, TypedDict

import pandas as pd

from vrp.loader import euclidean_distance


class Location(TypedDict):
    latitude: float
    longitude: float


class TruckState:
    IDLE = "idle"
    EN_ROUTE = "en_route"
    DELIVERING_LOAD = "delivering_load"
    FINISHED = "finished"


class Truck(TypedDict):
    id: int
    state: Literal["idle", "en_route", "delivering_load", "finished"]
    current_location: Location
    next_location: Optional[Location]
    dispatched_to_load: Optional[int]
    distance_travelled: float
    loads_handled: Optional[List[int]]


class LoadState:
    # The load is waiting for a truck to be assigned
    IDLE = "idle"
    # The load has a truck assigned
    EN_ROUTE = "en_route"
    # The load is on a truck and is being delivered
    DELIVERING = "delivering"


class Load(TypedDict):
    id: int
    pickup: Location
    dropoff: Location
    distance: float
    state: Literal["idle", "en_route", "delivering", "complete"]
    distance_to: Dict[str, float]
    origin_to_pickup_distance: float
    dropoff_to_origin_distance: float
    origin_to_pickup_to_dropoff: float


def row_to_type(row: pd.Series, tdClass: Type):
    return tdClass(**row.to_dict())  # type: ignore


class RouteData:
    def __init__(
        self, truck_count: int, df: pd.DataFrame, max_distance=12 * 60
    ) -> None:
        self._max_distance = max_distance
        self.trucks: List[Truck] = [
            Truck(
                id=id,
                state="idle",
                current_tocation=Location(latitude=0.0, longitude=0.0),
                next_tocation=None,
                dispatched_to_load=None,
                distance_travelled=0.0,
                loads_handled=None,
            )  # type: ignore
            for id in range(0, truck_count)
        ]
        self.loads: List[Load] = [
            Load(
                id=load.index.name,
                pickup=Location(**load["pickup"]),
                dropoff=Location(**load["dropoff"]),
                distance=load["distance"],
                state=LoadState.IDLE,
                distance_to=load["distanceTo"],
                origin_to_pickup_distance=load["originToPickupDistance"],
                dropoff_to_origin_distance=load["dropoffToOriginDistance"],
                origin_to_pickup_to_dropoff=load["originToPickupToDropoff"],
            )
            for _, load in df.iterrows()
        ]

        self._df_trucks: pd.DataFrame = pd.DataFrame(
            ([vars(truck) for truck in self.trucks])
        )
        self._df_loads: pd.DataFrame = pd.DataFrame(
            ([vars(load) for load in self.loads])
        )

    def _find_valid_combinations(
        self,
        df_available_loads: pd.DataFrame,
    ) -> Callable[[pd.Series], pd.Series]:

        def get_total_duration(
            truck_location: Location,
            pickup: Dict[str, float],
            distance: float,
            distance_to_origin: float,
        ) -> Dict[str, float]:
            distance_to_pickup = euclidean_distance(truck_location.__dict__, pickup)
            return {
                "job_distance": distance_to_pickup + distance,
                "distance_to_origin": distance_to_origin,
            }

        def can_be_completed_by(ds_truck: pd.Series) -> pd.Series:
            load_distances = df_available_loads.apply(
                lambda ds_load: get_total_duration(
                    ds_truck["current_location"],
                    ds_load["pickup"],
                    ds_load["distance"],
                    ds_load["dropoffToOriginDistance"],
                ),
                axis=1,
            )

            return ds_truck.combine_first(
                pd.Series(
                    {
                        "possible_loads": [
                            load
                            for load in load_distances
                            if ds_truck["distance_travelled"]
                            + load["job_distance"]
                            + load["distance_to_origin"]
                            < self._max_distance
                        ]
                    }
                )
            )

            available_loads.apply()
            loads = {load.index.name for _, load in available_loads.iterrows()}
            return ds.combine_first({})

        return load_validity

    # def get_available_options(self, minutes=0):

    #     # print(df.get(["pickup", "distance", "dropoffToOriginDistance"]))

    #     available_trucks = self._df_trucks[
    #         (self._df_trucks["state"] == TruckState.IDLE)
    #         & (self._df_trucks["distance"] < self._max_distance)
    #     ].apply((self.))
    #     available_loads = self._df_loads[(self._df_loads["state"] == LoadState.IDLE)]
