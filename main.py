"""
Street Network Map Generator
Generates a visualization of a place's street network using OSMnx.
"""

import osmnx as ox
from mcp.server.fastmcp import FastMCP

from maps import generators
from maps.types import (
    Address,
    GraphFromAddressOptions,
    GraphFromPlaceOptions,
    GraphFromPointOptions,
    OutputImageLocation,
    Place,
    PlotOptions,
    Point,
)

mcp = FastMCP(
    "Street map generator",
    dependencies=["maps@git+https://github.com/zzstoatzz/maps.git@mcp"],
)


@mcp.tool()
def plot_street_map_from_address(
    address: Address,
    address_options: GraphFromAddressOptions,
    output: OutputImageLocation,
    plot_options: PlotOptions,
) -> str:
    """Generate a street map from an address."""
    G = generators.from_address(address, **address_options)
    fig, _ = ox.plot_graph(G, **plot_options)
    fig.savefig(output, dpi=plot_options["dpi"])
    return "Map saved to " + output


@mcp.tool()
def plot_street_map_from_place(
    place: Place,
    place_options: GraphFromPlaceOptions,
    output: OutputImageLocation,
    plot_options: PlotOptions,
) -> str:
    """Generate a street map from a place."""
    G = generators.from_place(place, **place_options)
    fig, _ = ox.plot_graph(G, **plot_options)
    fig.savefig(output, dpi=plot_options["dpi"])
    return "Map saved to " + output


@mcp.tool()
def plot_street_map_from_point(
    point: Point,
    point_options: GraphFromPointOptions,
    output: OutputImageLocation,
    plot_options: PlotOptions,
) -> str:
    """Generate a street map from a point."""
    G = generators.from_point(point, **point_options)
    fig, _ = ox.plot_graph(G, **plot_options)
    fig.savefig(output, dpi=plot_options["dpi"])
    return "Map saved to " + output
