#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import re
from multiprocessing.pool import ThreadPool
from typing import Union

from more_itertools import bucket
from more_itertools import flatten
from pydantic import parse_obj_as
from tqdm import tqdm

from dims import config
from dims import ingest
from dims import models
from dims import output

# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


def parse_models(
    blob_data: ingest.BlobData,
) -> Union[
    list[models.LanderSaturn],
    list[models.LanderVenus],
    list[models.RocketSaturn],
    list[models.RocketVenus],
    list,
]:
    """Parse blob data into specified models.

    Args:
        blob_data (ingest.BlobData): A BlobData named tuple containing dictionary data.

    Returns:
        Union[list[models.LanderSaturn], list[models.LanderVenus],
        list[models.RocketSaturn], list[models.RocketVenus], list]:
            List of data parsed into correct model.

    """
    match blob_data:
        case blob_data if re.match(r".*lander_saturn.*", blob_data.name):
            return parse_obj_as(list[models.LanderSaturn], blob_data.data)
        case blob_data if re.match(r".*lander_venus.*", blob_data.name):
            return parse_obj_as(list[models.LanderVenus], blob_data.data)
        case blob_data if re.match(r".*rocket_saturn.*", blob_data.name):
            return parse_obj_as(list[models.RocketSaturn], blob_data.data)
        case blob_data if re.match(r".*rocket_venus.*", blob_data.name):
            return parse_obj_as(list[models.RocketVenus], blob_data.data)

    config.logger().error("File not parsed", file_name=blob_data.name)
    return []


def main() -> None:
    """Main entrypoint.

    This function
        - gets blob data using bucket name and max results from settings,
        - uses a thread pool to download and parse data, and
        - groups data by type and outputs it to CSV to the output directory
          given in settings.
    """
    settings = config.get_settings()
    blobs = list(ingest.get_blobs(settings.bucket, settings.max_results))

    with ThreadPool() as pool:
        craft_data = list(
            tqdm(
                pool.imap_unordered(ingest.get_blob_data, blobs),
                total=len(blobs),
                desc="Downloading data",
            )
        )
        parsed_crafts = list(
            tqdm(
                pool.imap_unordered(parse_models, craft_data),
                total=len(craft_data),
                desc="Parsing data",
            )
        )

    # Bucket by type name, e.g. LanderVenus.
    buckets = bucket(flatten(parsed_crafts), lambda craft: type(craft).__name__)
    for key in list(buckets):
        crafts = list(buckets[key])
        # Sort by timestamp because data might be
        # in any order after using imap_unordered.
        crafts.sort(key=lambda craft: craft.timestamp)
        output.crafts_to_csv(crafts, settings.output_dir / f"{key}.csv")


if __name__ == "__main__":  # pragma: no cover
    main()
