#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import pytest

from dims.config import get_settings

# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clear_cache():
    """Fixture clearing the get settings cache between test function invocations."""
    get_settings.cache_clear()
    yield


def test_config_default(monkeypatch):
    """Test the default configuration.

    With no env vars given, our settings should return default values.
    """
    monkeypatch.delenv("BUCKET", raising=False)
    settings = get_settings()
    assert settings.bucket == "de-assignment-data-bucket"


def test_config_env(monkeypatch):
    """Test configuration with env vars present.

    Our settings should return the value given in the relevant env vars.
    """
    bucket_name = "test_bucket"
    monkeypatch.setenv("BUCKET", bucket_name)
    settings = get_settings()
    assert settings.bucket == bucket_name
