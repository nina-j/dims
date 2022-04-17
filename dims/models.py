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
    class Config:
        allow_population_by_field_name: bool = True
        extra = "forbid"

    id: UUID
    size: str


class LanderSaturn(CraftBase):
    core: float
    speed: float = Field(alias="SPEED")
    force: float
    clones: int


class LanderVenus(CraftBase):
    core: float = Field(alias="coRe")
    suspension: float
    thrust: float
    weight: float
    crew: int


class RocketSaturn(CraftBase):
    mass: float = Field(alias="Mass")
    gravity: float
    temperature: float
    life: bool


class RocketVenus(CraftBase):
    speed: float
    axis_angle: float = Field(alias="axis_ANGLE")
