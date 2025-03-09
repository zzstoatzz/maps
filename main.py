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
    GraphFromPointOptions,
    PlotOptions,
    Point,
)

ox.settings.use_cache = False  # read-only fs inside MCP server # type: ignore

mcp = FastMCP(
    "Street map generator",
    dependencies=["maps@git+https://github.com/zzstoatzz/maps.git@mcp"],
)


def _make_url(key: str) -> str:
    return f"{r2_settings.R2_PUBLIC_BUCKET_URL}/{key}"


class R2Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    R2_BUCKET: str
    R2_ENDPOINT_URL: str
    R2_PUBLIC_BUCKET_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str


r2_settings = R2Settings()  # type: ignore

storage = R2Storage(
    bucket=r2_settings.R2_BUCKET,
    endpoint_url=r2_settings.R2_ENDPOINT_URL,
    aws_access_key_id=r2_settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=r2_settings.AWS_SECRET_ACCESS_KEY,
)


# @mcp.tool()
def plot_street_map_from_address(
    address: Address,
    address_options: GraphFromAddressOptions | None = None,
    plot_options: PlotOptions | None = None,
) -> str:
    """Generate a street map from an address."""
    address_options = address_options or {}
    plot_options = plot_options or {"node_size": 1}
    G = generators.from_address(address, **address_options)
    fig, _ = ox.plot_graph(G, show=False, **plot_options)
    key = storage.save_figure(
        fig,
        address_options.get("network_type", "street"),
        address.replace(",", "").replace(" ", "_"),
        plot_options.get("dpi", 300),
    )
    return _make_url(key)


@mcp.tool()
def plot_street_map_from_coordinates(
    point: Point,
    point_options: GraphFromPointOptions | None = None,
    plot_options: PlotOptions | None = None,
) -> str:
    """Generate a street map from a point."""
    point_options = point_options or {}
    plot_options = plot_options or {"node_size": 1}

    G = generators.from_point(point, **point_options)
    fig, _ = ox.plot_graph(G, show=False, **plot_options)
    key = storage.save_figure(
        fig,
        point_options.get("network_type", "street"),
        "some_coordinate_point",
        plot_options.get("dpi", 300),
    )
    return _make_url(key)


if __name__ == "__main__":
    print(plot_street_map_from_address("2530 16th St, San Francisco, CA 94103"))
