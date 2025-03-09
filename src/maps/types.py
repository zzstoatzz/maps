"""Highly annotated types for the maps package."""

from typing import Annotated, Literal, NotRequired, TypedDict

from pydantic import Field

Address = Annotated[
    str,
    Field(
        description="Address to generate the map from",
        examples=["123 Main St, Anytown, USA"],
    ),
]

Place = Annotated[
    str, Field(description="Place to generate the map from", examples=["Anytown, USA"])
]

Point = Annotated[
    tuple[float, float],
    Field(
        description="Point to generate the map from",
        examples=[(37.774929, -122.419418)],
    ),
]

OutputImageLocation = Annotated[
    str, Field(description="Path to save the output image", examples=["img/map.png"])
]


class PlotOptions(TypedDict):
    figsize: Annotated[tuple[float, float], Field(description="Size of the figure")]
    node_size: Annotated[int, Field(description="Size of the nodes")]
    dpi: Annotated[int, Field(description="Resolution of the output image")]
    edge_linewidth: Annotated[float, Field(description="Width of the edges")]
    bgcolor: Annotated[
        str,
        Field(description="(hex) Background color", examples=["#ffffff", "#000000"]),
    ]
    edge_color: Annotated[
        str,
        Field(description="(hex) Color of the edges", examples=["#ffffff", "#000000"]),
    ]
    show: Annotated[bool, Field(description="Whether to show the plot")]
    close: Annotated[bool, Field(description="Whether to close the plot")]


NetworkType = Literal["drive", "bike", "walk", "all"]


class _BaseFromOptions(TypedDict):
    network_type: NotRequired[
        Annotated[
            NetworkType,
            Field(description="Type of network to generate, defaults to 'all'"),
        ]
    ]
    simplify: NotRequired[
        Annotated[
            bool, Field(description="Whether to simplify the graph, defaults to True")
        ]
    ]
    retain_all: NotRequired[
        Annotated[
            bool, Field(description="Whether to retain all nodes, defaults to False")
        ]
    ]
    truncate_by_edge: NotRequired[
        Annotated[
            bool,
            Field(
                description="Whether to truncate the graph by edge, defaults to False"
            ),
        ]
    ]
    custom_filter: NotRequired[
        Annotated[
            str | list[str] | None,
            Field(description="Custom filter to use, defaults to None"),
        ]
    ]


class GraphFromAddressOptions(_BaseFromOptions):
    dist_type: NotRequired[
        Annotated[
            Literal["bbox", "network"],
            Field(description="Type of distance to use, defaults to 'bbox'"),
        ]
    ]


class GraphFromPlaceOptions(_BaseFromOptions):
    which_result: NotRequired[
        Annotated[
            int | None | list[int | None],
            Field(description="Which result to use, defaults to None"),
        ]
    ]


class GraphFromPointOptions(_BaseFromOptions):
    dist_type: NotRequired[
        Annotated[
            Literal["bbox", "network"],
            Field(description="Type of distance to use, defaults to 'bbox'"),
        ]
    ]
