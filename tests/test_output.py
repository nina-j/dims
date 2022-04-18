#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
from csv import DictReader

import pytest
from hypothesis import given
from hypothesis import strategies as st
from structlog.testing import capture_logs

from .test_models import craft_params
from .test_models import craft_strats
from dims.output import crafts_to_csv

# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(["model", "craft"], craft_params)
@given(strat_data=st.data())
def test_crafts_to_csv(model, craft, strat_data, temp_dir) -> None:
    """Test that we can write and read craft data from models.

    This test writes files to a temporary directory and reads them again to verify
    correctness.
    """
    model_data = strat_data.draw(craft_strats(craft))
    craft = model(**model_data)
    crafts = [craft] * 5
    test_file = temp_dir / "test.csv"
    crafts_to_csv(crafts, test_file)

    # Read data and verify
    from_csv = list(DictReader(test_file.open()))
    for craft, data in zip(crafts, from_csv):
        # CSV data is always all strings, all the time.
        assert list(map(str, craft.dict().values())) == list(data.values())


def test_crafts_to_csv_empty(temp_dir):
    test_file = temp_dir / "test.csv"
    with capture_logs() as log_output:
        crafts_to_csv([], test_file)
        assert {"event": "No data to output", "log_level": "warning"} in log_output
