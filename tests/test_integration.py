#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
from pathlib import Path

import pytest
from structlog.testing import capture_logs

from dims.ingest import BlobData
from dims.ingest import storage
from dims.main import config
from dims.main import main
from dims.main import parse_models

# --------------------------------------------------------------------------------------
# Code
# --------------------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def set_env(monkeypatch, temp_dir):
    monkeypatch.setattr(
        config, "get_settings", lambda *args: config.Settings(output_dir=temp_dir)
    )


def get_test_data(craft_type: str):
    data_dir = Path(__file__).parent / "test_data"
    match craft_type:
        case "lander_saturn":
            file_name = "lander_saturn_20210301_013306.csv"
            return file_name, (data_dir / file_name).read_bytes()
        case "lander_venus":
            file_name = "lander_venus_20210301_003124.csv"
            return file_name, (data_dir / file_name).read_bytes()
        case "rocket_saturn":
            file_name = "rocket_saturn_20210301_121033.csv"
            return file_name, (data_dir / file_name).read_bytes()
        case "rocket_venus":
            file_name = "rocket_venus_20210308_035720.csv"
            return (file_name, (data_dir / file_name).read_bytes())


@pytest.mark.parametrize(
    "craft_type", ["lander_saturn", "lander_venus", "rocket_saturn", "rocket_venus"]
)
def test_integration_main(monkeypatch, craft_type, temp_dir):
    file_name, csv_bytes = get_test_data(craft_type)

    monkeypatch.setattr(
        storage.Blob,
        "download_as_bytes",
        lambda *args, **kwargs: csv_bytes,
    )
    monkeypatch.setattr(
        storage.Client,
        "list_blobs",
        lambda *args: [storage.Blob(file_name, "test_bucket")],
    )
    main()
    result_files = list(Path(temp_dir).glob("*"))
    for result_file in result_files:
        with result_file.open() as f:
            assert len(f.readlines()) == 1001  # header + 1000 data lines


def test_parse_models():
    name = "test"
    blob_data = BlobData(name=name, data=[{"fake": "data"}])
    with capture_logs() as log_output:
        result = parse_models(blob_data)
        assert result == []
        assert {
            "file_name": name,
            "event": "File not parsed",
            "log_level": "error",
        } in log_output
