from dataclasses import dataclass, field
from typing import Optional

from vrp.common.types.coordinate_vector import CoordinateVector


@dataclass(frozen=True)
class DeliveryLoad(CoordinateVector):
    load_number: int
    visited_by: Optional[int] = field(init=False, repr=True, default=None)

    def __post_init__(self):
        object.__setattr__(self, "visited_by", None)
        object.__setattr__(self, "connections", [])

    def visit(self, by: int) -> "DeliveryLoad":
        object.__setattr__(self, "visited_by", by)
        return self
