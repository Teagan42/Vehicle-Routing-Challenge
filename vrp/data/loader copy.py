import pandas as pd

from vrp.calculations import cartesian_distance
from vrp.load.location import Location

LOCATION_COLUMNS = ["pickup", "dropoff"]


class DataLoader:
    """Loads data from delimited files into dataframes."""

    def _parse_location(self, location: str) -> Location:
        return Location(*map(float, location.strip("()").split(",")))

    def _process_row(self, ds: pd.Series) -> pd.Series:
        locations = {
            column: self._parse_location(ds[column]) for column in LOCATION_COLUMNS
        }
        return pd.Series(
            {
                "load_number": ds["loadNumber"],
                "pickup_latitude": locations["pickup"].latitude,
                "pickup_longitude": locations["pickup"].longitude,
                "dropoff_latitude": locations["dropoff"].latitude,
                "dropoff_longitude": locations["dropoff"].longitude,
                "distance": cartesian_distance(
                    locations["pickup"], locations["dropoff"]
                ),
            }
        )

    def readFile(self, file_path: str, delimiter: str = ",") -> pd.DataFrame:
        df = pd.read_csv(file_path, delimiter=delimiter)
        return df.apply(self._process_row, axis=1)
