#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import csv
from collections.abc import Iterator
from io import StringIO
from typing import Any
from typing import NamedTuple

from google.cloud import storage

from .config import logger

# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


class BlobData(NamedTuple):
    """Collection of BlobData."""

    name: str
    data: list[dict[str, Any]]


def get_blobs(
    bucket_name: str, max_results: int | None = None
) -> Iterator[storage.Blob]:
    """Get blobs from a public bucket using an anonymous gcp client.

    Args:
        bucket_name (str): Name of the bucket to get blobs from.
        max_results (int | None, optional): Maximum number of blobs to return.
            Defaults to None.

    Returns:
        Iterator[storage.Blob]: An iterator of blobs in the given bucket.
    """
    client = storage.Client.create_anonymous_client()
    return client.list_blobs(bucket_name, max_results)


def get_blob_data(blob: storage.Blob) -> BlobData:
    """Get csv file names and data in dictionary format from a given blob.

    Args:
        blob (storage.Blob): The blob to download data from.

    Returns:
        BlobData: A NamedTuple containing the blob name and a list of dictionary data.
    """
    raw_data = blob.download_as_bytes()

    try:
        blob_data = list(csv.DictReader(StringIO(raw_data.decode())))
    except csv.Error as e:
        logger().error("Failed to parse blob data", error=str(e))
        blob_data = []

    return BlobData(blob.name, blob_data)
