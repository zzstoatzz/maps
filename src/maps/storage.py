"""Storage utilities for map images."""

import io
from datetime import datetime
from typing import Any

import boto3
import matplotlib.figure as mpl_fig
from botocore.config import Config


class R2Bucket:
    """Handles storing map images in Cloudflare R2."""

    def __init__(
        self,
        bucket_name: str,
        endpoint_url: str,
        region_name: str = "auto",
        **credentials: Any,
    ) -> None:
        """Initialize R2 storage client.

        Args:
            bucket: R2 bucket name
            endpoint_url: R2 endpoint URL
            region_name: R2 region name
            **credentials: AWS credentials (access_key_id, secret_access_key)
        """
        self.bucket_name = bucket_name
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            region_name=region_name,
            config=Config(
                request_checksum_calculation="WHEN_REQUIRED",
                response_checksum_validation="WHEN_REQUIRED",
            ),
            **credentials,
        )

    def upload_fileobj(
        self,
        fileobj: io.BytesIO,
        key: str,
    ) -> None:
        """Upload a file object to R2."""
        self.client.upload_fileobj(fileobj, self.bucket_name, key)

    def save_figure(
        self,
        fig: mpl_fig.Figure,
        network_type: str,
        namespace: str,
        dpi: int = 300,
    ) -> str:
        """Save matplotlib figure to R2.

        Args:
            fig: Matplotlib figure to save
            network_type: Type of network (for filename)
            dpi: DPI for saved image

        Returns:
            key of newly created object in R2
        """
        # Create buffer and save figure to it
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=dpi, bbox_inches="tight")
        buf.seek(0)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        key = f"{namespace}/{network_type}_{timestamp}.png"

        self.upload_fileobj(buf, key)

        return key
