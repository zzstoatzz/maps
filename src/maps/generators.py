"""Graph generators for different data sources."""

from typing import Unpack

import osmnx as ox
from networkx import MultiDiGraph

from maps.types import (
    GraphFromAddressOptions,
    GraphFromPlaceOptions,
    GraphFromPointOptions,
)


def from_address(
    address: str,
    dist: int = 1000,
    **kwargs: Unpack[GraphFromAddressOptions],
) -> MultiDiGraph:
    """Generate a street network graph from an address.

    Args:
        address: The address to generate the graph from
        network_type: Type of network to generate
        dist: Distance in meters to search from the address

    Returns:
        A NetworkX MultiDiGraph representing the street network
    """
    G = ox.graph_from_address(
        address,
        dist=dist,
        **kwargs,
    )
    assert isinstance(G, MultiDiGraph)
    return G


def from_place(
    place: str | dict[str, str] | list[str | dict[str, str]],
    **kwargs: Unpack[GraphFromPlaceOptions],
) -> MultiDiGraph:
    """Generate a street network graph from a place name.

    Args:
        place: Place name or dict with keys 'city', 'state', 'country'
        network_type: Type of network to generate

    Returns:
        A NetworkX MultiDiGraph representing the street network
    """
    return ox.graph_from_place(place, **kwargs)


def from_point(
    point: tuple[float, float],
    dist: int = 1000,
    **kwargs: Unpack[GraphFromPointOptions],
) -> MultiDiGraph:
    """Generate a street network graph from a lat/lon point.

    Args:
        point: (latitude, longitude) tuple
        dist: Distance in meters to search from the point
        network_type: Type of network to generate

    Returns:
        A NetworkX MultiDiGraph representing the street network
    """
    return ox.graph_from_point(point, dist=dist, **kwargs)
