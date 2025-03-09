# /// script
# dependencies = ["maps@git+https://github.com/zzstoatzz/maps.git"]
# ///
"""
Street Network Map Generator
Generates a visualization of a place's street network using OSMnx.
"""

import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import osmnx as ox


def generate_street_map(
    place: str,
    network_type: str = "drive",
    save_path: str | None = None,
    figsize: tuple[int, int] = (12, 10),
    dpi: int = 300,
    edge_linewidth: float = 0.5,
    node_size: int = 0,
    bgcolor: str = "black",
    edge_color: str = "white",
) -> None:
    """
    Generate and save a map of a street network.

    Args:
        place: Name of the place to download the street network
        network_type: Type of street network ('drive', 'bike', 'walk', or 'all')
        save_path: Path to save the output image (None for display only)
        figsize: Figure dimensions in inches
        dpi: Resolution of output image
        edge_linewidth: Width of the street lines
        node_size: Size of intersection nodes (0 to hide)
        bgcolor: Background color of the map
        edge_color: Color of the street lines
    """
    print(f"Downloading street network for {place} (type: {network_type})...")
    graph = ox.graph_from_place(place, network_type=network_type)
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


if __name__ == "__main__":
    place = sys.argv[1] if len(sys.argv) > 1 else "Chicago, Illinois, USA"
    network = sys.argv[2] if len(sys.argv) > 2 else "drive"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"street_map_{timestamp}.png"

    output = f"{network}_{output_path}"
    generate_street_map(
        place=place,
        network_type=network,
        save_path=output,
        edge_color="#ffffff"
        if network == "drive"
        else "#3498db"
        if network == "bike"
        else "#2ecc71",
    )
    print(f"Created {network} network map: {output}")

    print("All maps generated successfully!")
