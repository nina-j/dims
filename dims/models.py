#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field

# --------------------------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------------------------


class CraftBase(BaseModel):
    """Base craft data model."""

    class Config:
        allow_population_by_field_name: bool = True
        extra = "forbid"

    id: UUID
    size: str


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
