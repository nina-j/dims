#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

# --------------------------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------------------------


class CraftBase(BaseModel):
    """Base craft data model."""

    class Config:
        allow_population_by_field_name: bool = True
        extra = "forbid"
        json_encoders = {datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")}

    id: UUID
    size: str
    timestamp: datetime

    @validator("timestamp", pre=True)
    def timestamp_from_string(cls, string: str) -> datetime:
        """Extract timestamp from a string on the form .*yyyyMMdd_HHmmss.

        Args:
            string (str): String to extract timestamp from.

        Returns:
            datetime: Parsed timestamp as a datetime.
        """
        timestamp = "".join(re.findall(r"\d{8}_\d{6}$", string))
        return datetime.strptime(timestamp, "%Y%m%d_%H%M%S")


class LanderSaturn(CraftBase):
    """Saturn lander data model."""

    core: float
    speed: float = Field(alias="SPEED")
    force: float
    clones: int


class LanderVenus(CraftBase):
    """Venus lander data model."""

    core: float = Field(alias="coRe")
    suspension: float
    thrust: float
    weight: float
    crew: int


class RocketSaturn(CraftBase):
    """Saturn rocket data model."""

    mass: float = Field(alias="Mass")
    gravity: float
    temperature: float
    life: bool


class RocketVenus(CraftBase):
    """Venus rocket data model."""

    speed: float
    axis_angle: float = Field(alias="axis_ANGLE")
