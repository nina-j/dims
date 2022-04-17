#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import csv
from pathlib import Path

from .models import CraftBase
from dims.config import logger

# --------------------------------------------------------------------------------------
# Output CSV
# --------------------------------------------------------------------------------------


def crafts_to_csv(models: list[CraftBase], out_file: Path) -> None:
    """Generate csv file from craft model data.

    Args:
        models (list[CraftBase]): Crafts to output
        out_file (Path): File to output data to.
    """
    if not models:
        logger().warn("No data to output")
        return None

    fieldnames = models[0].__fields__
    with out_file.open("w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, escapechar="\n")
        writer.writeheader()
        writer.writerows([model.dict() for model in models])
