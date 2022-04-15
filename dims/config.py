#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
from functools import lru_cache

import structlog
from pydantic import BaseSettings

# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


class Settings(BaseSettings):
    """Settings via environment variables for use throughout the project."""

    bucket: str = "de-assignment-data-bucket"


@lru_cache(maxsize=32)
def get_settings() -> Settings:
    """Initialise & LRU cache settings.

    Returns:
        Settings: Settings with values from the environment.
    """
    return Settings()


def logger() -> structlog.stdlib.BoundLogger:
    """Get a BoundLogger from structlog.

    Returns:
        structlog.stdlib.BoundLogger: A BoundLogger for structured logging.
    """
    return structlog.stdlib.get_logger()
