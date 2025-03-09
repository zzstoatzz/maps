"""
Street Network Map Generator
Generates a visualization of a place's street network using OSMnx.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal

import osmnx as ox
from mcp.server.fastmcp import FastMCP
from pydantic_settings import BaseSettings, SettingsConfigDict

from maps import generators
from maps.storage import R2Bucket
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
    instructions=(
        "use to create street maps from addresses or coordinates, "
        "show urls from the tools to the user. default to walking paths "
        "unless otherwise requested. "
    ),
    dependencies=["maps[storage]@git+https://github.com/zzstoatzz/maps.git@mcp"],
)


def _make_url(key: str) -> str:
    return f"{r2_bucket_settings.R2_PUBLIC_BUCKET_URL}/{key}"


class R2BucketSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    R2_BUCKET: str
    R2_ENDPOINT_URL: str
    R2_PUBLIC_BUCKET_URL: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str


r2_bucket_settings = R2BucketSettings()  # type: ignore

r2_bucket = R2Bucket(
    bucket_name=r2_bucket_settings.R2_BUCKET,
    endpoint_url=r2_bucket_settings.R2_ENDPOINT_URL,
    aws_access_key_id=r2_bucket_settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=r2_bucket_settings.AWS_SECRET_ACCESS_KEY,
)


@mcp.tool()
def plot_street_map_from_address(
    address: Address,
    address_options: GraphFromAddressOptions | None = None,
    plot_options: PlotOptions | None = None,
) -> str:
    """Generate a street map from an address."""
    address_options = address_options or {}
    plot_options = plot_options or {"node_size": 1, "edge_linewidth": 0.5}
    G = generators.from_address(address, **address_options)
    fig, _ = ox.plot_graph(G, show=False, **plot_options)
    key = r2_bucket.save_figure(
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
    plot_options = plot_options or {"node_size": 1, "edge_linewidth": 0.5}

    G = generators.from_point(point, **point_options)
    fig, _ = ox.plot_graph(G, show=False, **plot_options)
    key = r2_bucket.save_figure(
        fig,
        point_options.get("network_type", "street"),
        "some_coordinate_point",
        plot_options.get("dpi", 300),
    )
    return _make_url(key)


def generate_street_map_from_address(
    address: str,
    network_type: Literal["drive", "bike", "walk", "all"] = "drive",
    save_path: Path | str | None = None,
    figsize: tuple[int, int] = (12, 10),
    dpi: int = 300,
    edge_linewidth: float = 0.5,
    node_size: int = 0,
    bgcolor: str = "black",
    edge_color: str = "white",
    dist: int = 5000,
) -> None:
    """this is just here because this is the way it worked when I made this post on bsky
    and so if someone tries to run it like i did in the post, it'll still work

    https://bsky.app/profile/did:plc:xbtmt2zjwlrfegqvch7fboei/post/3ljvxn7dy3c2l
    """
    import matplotlib.pyplot as plt

    print(f"Downloading street network for {address} (type: {network_type})...")
    graph = ox.graph_from_address(address, network_type=network_type, dist=dist)
    graph_proj = ox.project_graph(graph)  # type: ignore

    print("Generating map visualization...")
    fig, _ = ox.plot_graph(
        graph_proj,
        figsize=figsize,
        node_size=node_size,
        edge_linewidth=edge_linewidth,
        bgcolor=bgcolor,
        edge_color=edge_color,
        show=False,
        close=False,
    )

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        print(f"Saving map to {save_path}...")
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")
        plt.close()
    else:
        print("Displaying map...")
        plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate street network maps using OSMnx",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "address",
        type=str,
        nargs="?",  # Make address optional
        help="Address to generate map for",
    )
    parser.add_argument(
        "--server",
        action="store_true",
        help="Run as MCP server instead of CLI tool",
    )
    parser.add_argument(
        "--network-type",
        type=str,
        choices=["drive", "bike", "walk", "all"],
        default="drive",
        help="Type of network to generate",
    )
    parser.add_argument(
        "--dist",
        type=int,
        default=5000,
        help="Distance in meters to search from the place",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution of output image",
    )
    parser.add_argument(
        "--edge-linewidth",
        type=float,
        default=0.5,
        help="Width of the street lines",
    )
    parser.add_argument(
        "--node-size",
        type=int,
        default=0,
        help="Size of intersection nodes (0 to hide)",
    )
    parser.add_argument(
        "--bgcolor",
        type=str,
        default="black",
        help="Background color of the map",
    )
    parser.add_argument(
        "--edge-color",
        type=str,
        help="Color of the street lines (defaults based on network type)",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (defaults to street_map_TIMESTAMP.png)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Run server if no args provided or --server flag is used
    if len(sys.argv) == 1 or args.server:
        mcp.run()
    else:
        # Handle CLI usage
        if not args.edge_color:
            args.edge_color = {
                "drive": "#ffffff",
                "bike": "#3498db",
                "walk": "#2ecc71",
                "all": "#ffffff",
            }[args.network_type]

        if not args.output:
            output_dir = Path("img")
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            args.output = output_dir / f"{args.network_type}_street_map_{timestamp}.png"

        generate_street_map_from_address(
            address=args.address,
            network_type=args.network_type,
            save_path=args.output,
            dpi=args.dpi,
            edge_linewidth=args.edge_linewidth,
            node_size=args.node_size,
            bgcolor=args.bgcolor,
            edge_color=args.edge_color,
            dist=args.dist,
        )
        print("Map generated successfully!")
