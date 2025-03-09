# /// script
# dependencies = ["maps@git+https://github.com/zzstoatzz/maps.git"]
# ///
"""
Street Network Map Generator
Generates a visualization of a place's street network using OSMnx.
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
import osmnx as ox


def generate_street_map_from_address(
    address: str,
    network_type: Literal["drive", "bike", "walk", "all"] = "drive",
    save_path: str | None = None,
    figsize: tuple[int, int] = (12, 10),
    dpi: int = 300,
    edge_linewidth: float = 0.5,
    node_size: int = 0,
    bgcolor: str = "black",
    edge_color: str = "white",
    dist: int = 5000,
) -> None:
    """
    Generate and save a map of a street network.

    Args:
        address: Address to download the street network
        network_type: Type of street network ('drive', 'bike', 'walk', or 'all')
        save_path: Path to save the output image (None for display only)
        figsize: Figure dimensions in inches
        dpi: Resolution of output image
        edge_linewidth: Width of the street lines
        node_size: Size of intersection nodes (0 to hide)
        bgcolor: Background color of the map
        edge_color: Color of the street lines
        dist: Distance in meters to search from the place
    """
    print(f"Downloading street network for {address} (type: {network_type})...")
    graph = ox.graph_from_address(address, network_type=network_type, dist=dist)
    graph_proj = ox.project_graph(graph)

    print("Generating map visualization...")
    fig, ax = ox.plot_graph(
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
        help="Address to generate map for",
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

    # Set default edge colors based on network type if not specified
    if not args.edge_color:
        args.edge_color = {
            "drive": "#ffffff",
            "bike": "#3498db",
            "walk": "#2ecc71",
            "all": "#ffffff",
        }[args.network_type]

    # Generate default output path if not specified
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"{args.network_type}_street_map_{timestamp}.png"

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
