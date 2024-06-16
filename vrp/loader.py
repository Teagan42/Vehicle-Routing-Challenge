from typing import Callable, Dict

import pandas as pd
from numpy import sqrt

from vrp.const import ORIGIN


def _parse_coordinate(coordinateString: str) -> Dict[str, float]:
    """
    Parses a coordinate string into a dictionary of it's consituant parts.

    Args:
        location (str): Latitude and Longitude separated by a ',' with or without being wrapped in parenthesis

    Returns:
        Dict[str, float]: Dictionary with 'latitude' and 'longitude' keys and float values
    """
    latitude, longitude = map(float, coordinateString.strip("()").split(","))
    return {"latitude": latitude, "longitude": longitude}


def euclidean_distance(a: Dict[str, float], b: Dict[str, float]) -> float:
    """
    Calculate the Euclidean distance between two locations.
    """
    return sqrt(
        (a["latitude"] - b["latitude"]) ** 2 + (a["longitude"] - b["longitude"]) ** 2
    )


def get_distances(
    df: pd.DataFrame, current: Dict[str, float] = ORIGIN
) -> Callable[[pd.Series], pd.Series]:
    """
    Returns a function that adds a set of 'distance' columns with the calculated Euclidean distance as values

    Args:
        df (pd.DataFrame): The DataFrame containing the set of loads

    Returns:
        Callable[[pd.Series], pd.Series]: The method to apply to each series in the DataFrame
    """

    def add_distance_to(ds: pd.Series) -> pd.Series:
        """
        Adds the following columns to the series:
            * distance: the Euclidean distance from pickup to drop off
            * originToPickupDistance: the Euclidean distance from origin to pickup
            * dropoffToOriginDistance: the Euclidean distance from dropoff to origin
            * originToPickupToDropoff: The total distance this load would starting from the origin
            * distanceTo: Dictionary with loadNumber as key and the Euclidean distance from 'dropoff' to the other load's 'pickup'

        Args:
            ds (pd.Series): A series from the load dataset

        Returns:
            pd.Series: The series with the added distance columns
        """
        distance = euclidean_distance(ds["pickup"], ds["dropoff"])
        originToPickupDistance = euclidean_distance(ORIGIN, ds["pickup"])
        distances = {
            "distance": distance,
            "originToPickupDistance": originToPickupDistance,
            "dropoffToOriginDistance": euclidean_distance(ds["dropoff"], ORIGIN),
            "originToPickupToDropoff": distance + originToPickupDistance,
            "distanceTo": {
                id: euclidean_distance(ds["dropoff"], dsLoad["pickup"])
                for id, dsLoad in df.iterrows()
                if dsLoad.name != ds.name
            },
        }

        print(ds)
        return ds.combine_first(pd.Series(distances))

    return add_distance_to


def read_loads_file(file_path: str, delimiter=" ") -> pd.DataFrame:
    """
    Reads a loads file into a DataFrame, adding a 'distance' column with the calculated Euclidean distance between 'pickup' and 'dropoff' columns.

    Args:
        file_path (str): the path to the file containing the set of loads

    Returns:
        pd.DataFrame: DataFrame with index 'loadNumber', columns 'pickup' and 'dropoff' separated into latitude and longitude, and 'distance' column calcualted from 'pickup' and 'dropoff'
    """
    df = pd.read_csv(
        file_path,
        delimiter=delimiter,
        index_col="loadNumber",
        converters={
            "pickup": _parse_coordinate,
            "dropoff": _parse_coordinate,
        },
    )

    return df.apply(get_distances(df), axis=1).sort_values(
        by="originToPickupToDropoff", ascending=False
    )
