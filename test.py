import pandas as pd

from vrp.loader import read_loads_file
from vrp.route.data import LoadState, Location

df: pd.DataFrame = read_loads_file("data/problem1.txt")

print(df)
[
    print(
        {
            "name": load.name,
            "id": index,
            "pickup": Location(**load["pickup"]),
            "dropoff": Location(**load["dropoff"]),
            "distance": load["distance"],
            "state": LoadState.IDLE,
            "distanceTo": load["distanceTo"],
            "originToPickupDistance": load["originToPickupDistance"],
            "dropoffToOriginDistance": load["dropoffToOriginDistance"],
        }
    )
    for index, load in df.iterrows()
]

print(df.get(["pickup", "distance", "dropoffToOriginDistance"]))
