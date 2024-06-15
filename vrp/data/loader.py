import pandas as pd

from vrp.calculations import cartesian_distance
from vrp.load.load import Load
from vrp.load.location import Location

Load._fields

LOCATION_COLUMNS = [
    field for field in Load._fields if Load.__annotations__[field] is Location
]


class DataLoader:

    def _parse_location(self, location: str) -> Location:
        lat, long = map(float, location.strip("()").split(","))
        return Location(latitude=lat, longitude=long)

    def _add_distance(self, ds: pd.Series) -> pd.Series:
        return ds.combine_first(
            pd.Series(
                {
                    "distance": cartesian_distance(
                        *[ds[column] for column in LOCATION_COLUMNS]
                    )
                }
            )
        )

    def readFile(self, file_path: str) -> pd.DataFrame:
        df = pd.read_csv(
            file_path,
            delim_whitespace=True,
            index_col="loadNumber",
            converters={column: self._parse_location for column in LOCATION_COLUMNS},
        )

        return df.apply(self._add_distance, axis=1)
