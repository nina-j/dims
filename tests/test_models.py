#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from dims.models import CraftBase
from dims.models import LanderSaturn
from dims.models import LanderVenus
from dims.models import RocketSaturn
from dims.models import RocketVenus

# --------------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------------


def base_strat() -> st.SearchStrategy:
    """Strategy for generating CraftBase dictionary data."""
    size_strat = st.one_of(st.text(), st.integers().map(str))
    required = {"id": st.uuids(), "size": size_strat}
    return st.fixed_dictionaries(required)


@given(model_data=base_strat())
def test_base_model(model_data: dict[str, str]) -> None:
    """Test that we can parse data to the CraftBase model."""
    assert CraftBase(**model_data)


@st.composite
def craft_strats(
    draw: st.DrawFn, craft: dict[str, st.SearchStrategy]
) -> dict[str, Any]:
    """Strategy for generating different craft dictionary data.

    They all share base data, so first we draw from the base strat,
    then from fixed dictionaries given by the `craft` parameter.
    """
    return {**draw(base_strat()), **draw(st.fixed_dictionaries(craft))}


# Params for parametrized craft model test.
craft_params = [
    (
        LanderSaturn,
        {
            "core": st.floats(),
            "SPEED": st.floats(),
            "force": st.floats(),
            "clones": st.integers(),
        },
    ),
    (
        LanderVenus,
        {
            "coRe": st.floats(),
            "suspension": st.floats(),
            "thrust": st.floats(),
            "weight": st.floats(),
            "crew": st.integers(),
        },
    ),
    (
        RocketSaturn,
        {
            "Mass": st.floats(),
            "gravity": st.floats(),
            "temperature": st.floats(),
            "life": st.booleans(),
        },
    ),
    (RocketVenus, {"speed": st.floats(), "axis_ANGLE": st.floats()}),
]


@pytest.mark.parametrize(["model", "craft"], craft_params)
@given(strat_data=st.data())
def test_crafts(model, craft, strat_data) -> None:
    """Test that we can parse data to the different craft models.

    This test also confirms that our aliases work as expected.
    """
    model_data = strat_data.draw(craft_strats(craft))
    assert model(**model_data)
