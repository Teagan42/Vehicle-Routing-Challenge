"""Various Simple Routing Strategies."""

from .least_stops_strategy import LeastStopsRoutingStrategy
from .nearest_neighbor_strategy import NearestNeighborRoutingStrategy
from .nearest_shortest_job_strategy import NearestShortestJobRoutingStrategy
from .shortest_job_strategy import ShortestJobRoutingStrategy
from .base_strategy import BaseRoutingStrategy


RoutingStrategy = BaseRoutingStrategy
LeastStopsStrategy = LeastStopsRoutingStrategy
NearestNeighborStrategy = NearestNeighborRoutingStrategy
NearestAndShortestJobStrategy = NearestShortestJobRoutingStrategy
ShortedJobStrategy = ShortestJobRoutingStrategy

routing_strategies = [
    # LeastStopsStrategy,
    # NearestNeighborStrategy,
    NearestAndShortestJobStrategy,
    ShortedJobStrategy,
]
