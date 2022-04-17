#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import csv
from collections.abc import Iterator
from io import StringIO

from google.cloud import storage

from .config import logger

# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


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


def get_blob_data(blob: storage.Blob) -> list[dict[str, str]]:
    """Get csv file names and data in dictionary format from a given blob.

    Args:
        blob (storage.Blob): The blob to download data from.

    Returns:
        list[dict[str, str]]: A list containing a dictionary representation of csv data.
    """
    raw_data = blob.download_as_bytes()
    try:
        csv_data: list[dict[str, str]] = list(
            csv.DictReader(StringIO(raw_data.decode()))
        )
    except csv.Error as e:
        logger().error("Failed to parse blob data", error=str(e))
        return []
    else:
        for data in csv_data:
            data.setdefault("timestamp", blob.name)
    return csv_data
