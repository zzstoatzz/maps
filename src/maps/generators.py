"""Graph generators for different data sources."""

from typing import Unpack

import osmnx as ox
from networkx import MultiDiGraph

from maps.types import (
    Address,
    GraphFromAddressOptions,
    GraphFromPlaceOptions,
    GraphFromPointOptions,
    Place,
    Point,
)


def from_address(
    address: Address,
    dist: int = 1000,
    **kwargs: Unpack[GraphFromAddressOptions],
) -> MultiDiGraph:
    """Generate a street network graph from an address.

    Args:
        address: The address to generate the graph from
        network_type: Type of network to generate
        dist: Distance in meters to search from the address

    Returns:
        A NetworkX MultiDiGraph representing the street network (projected to UTM)
    """
    G = ox.graph_from_address(
        address,
        dist=dist,
        **kwargs,
    )
    assert isinstance(G, MultiDiGraph)
    return ox.project_graph(G)


def from_place(
    place: Place,
    **kwargs: Unpack[GraphFromPlaceOptions],
) -> MultiDiGraph:
    """Generate a street network graph from a place name.

    Args:
        place: Place name or dict with keys 'city', 'state', 'country'
        network_type: Type of network to generate

    Returns:
        A NetworkX MultiDiGraph representing the street network (projected to UTM)
    """
    G = ox.graph_from_place(place, **kwargs)
    return ox.project_graph(G)


def from_point(
    point: Point,
    dist: int = 1000,
    **kwargs: Unpack[GraphFromPointOptions],
) -> MultiDiGraph:
    """Generate a street network graph from a lat/lon point.

    Args:
        point: (latitude, longitude) tuple
        dist: Distance in meters to search from the point
        network_type: Type of network to generate

    Returns:
        A NetworkX MultiDiGraph representing the street network (projected to UTM)
    """
    G = ox.graph_from_point(point, dist=dist, **kwargs)
    return ox.project_graph(G)
