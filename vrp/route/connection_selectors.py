from random import randint
from typing import List

from vrp.common.calculations import euclidean_distance
from vrp.common.types.delivery_load_connection import DeliveryLoadConnection
from vrp.common.types.truck import Truck


def _random(truck: Truck, connections: List[DeliveryLoadConnection]) -> DeliveryLoadConnection:
    for i in range(0, len(connections)):
        connection = connections[randint(0, len(connections))]
        truck_distance = euclidean_distance(truck.location, connection)
        if connection.distance + connection.end.distance_from_origin


def _longest(connections: List[DeliveryLoadConnection]) -> DeliveryLoadConnection:
    connections.sort(key=lambda c: c.distance, reverse=True)
    return connections[0]


def _shortest(connections: List[DeliveryLoadConnection]) -> DeliveryLoadConnection:
    connections.sort(key=lambda c: c.distance, reverse=False)
    return connections[0]


ConnectionSelectors = {"random": _random, "lngest": _longest, "shortest": _shortest}
