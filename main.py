"""
Street Network Map Generator
Generates a visualization of a place's street network using OSMnx.
"""

import osmnx as ox
from mcp.server.fastmcp import FastMCP
from pydantic_settings import BaseSettings, SettingsConfigDict

from maps import generators
from maps.storage import R2Storage
from maps.types import (
    Address,
    GraphFromAddressOptions,
    GraphFromPlaceOptions,
    GraphFromPointOptions,
    Place,
    PlotOptions,
    Point,
)

ox.settings.use_cache = False

mcp = FastMCP(
    "Street map generator",
    dependencies=["maps@git+https://github.com/zzstoatzz/maps.git@mcp"],
)


class R2Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    R2_BUCKET: str
    R2_ENDPOINT_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str


r2_settings = R2Settings()  # type: ignore

storage = R2Storage(
    bucket=r2_settings.R2_BUCKET,
    endpoint_url=r2_settings.R2_ENDPOINT_URL,
    aws_access_key_id=r2_settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=r2_settings.AWS_SECRET_ACCESS_KEY,
)


@mcp.tool()
def plot_street_map_from_address(
    address: Address,
    address_options: GraphFromAddressOptions,
    plot_options: PlotOptions,
) -> str:
    """Generate a street map from an address."""
    G = generators.from_address(address, **address_options)
    fig, _ = ox.plot_graph(G, **plot_options)
    return storage.save_figure(
        fig, address_options.get("network_type", "street"), plot_options["dpi"]
    )


@mcp.tool()
def plot_street_map_from_place(
    place: Place,
    place_options: GraphFromPlaceOptions,
    plot_options: PlotOptions,
) -> str:
    """Generate a street map from a place."""
    G = generators.from_place(place, **place_options)
    fig, _ = ox.plot_graph(G, **plot_options)
    return storage.save_figure(
        fig, place_options.get("network_type", "street"), plot_options["dpi"]
    )


@mcp.tool()
def plot_street_map_from_point(
    point: Point,
    point_options: GraphFromPointOptions,
    plot_options: PlotOptions,
) -> str:
    """Generate a street map from a point."""
    G = generators.from_point(point, **point_options)
    fig, _ = ox.plot_graph(G, **plot_options)
    return storage.save_figure(
        fig, point_options.get("network_type", "street"), plot_options["dpi"]
    )
