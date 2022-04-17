#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import re
from datetime import datetime
from typing import Literal
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

    id: str
    magnitude: Literal["massive", "big", "medium", "small", "tiny", "N/A"] = Field(
        alias="size"
    )
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

    @validator("id", pre=True)
    def id_from_uuid(cls, uuid_: UUID | str) -> str:
        """Parse an UUID into an ID using the middle value.

        For example: f0388371-7285-449c-be70-277db541ac86 -> 449c

        Args:
            uuid_ (UUID | str): The incoming UUID to parse.

        Returns:
            str: A string of length 4 corresponding to the middle value.
        """
        if isinstance(uuid_, str):
            uuid_ = UUID(uuid_)
        # UUID.fields gives integer values - hex format them.
        return f"{uuid_.fields[2]:x}"

    @validator("magnitude", pre=True)
    def size_to_magnitude(
        cls, size: str
    ) -> Literal["massive", "big", "medium", "small", "tiny", "N/A"]:
        """Parse a size string into a magnitude.

        Args:
            size (str): The size to parse.

        Returns:
            Literal["massive", "big", "medium", "small", "tiny", "N/A"]:
                Magnitude matched on size.
        """
        try:
            size_int = int(size)
        except ValueError:
            return "N/A"

        match size_int:
            case x if 500 <= x < 1000:
                return "massive"
            case x if 100 <= x < 500:
                return "big"
            case x if 50 <= x < 100:
                return "small"
            case x if 1 <= x < 50:
                return "tiny"

        # We should be able to just match the wildcard case _
        # and return "N/A", but mypy doesn't understand it. >:(
        return "N/A"


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
