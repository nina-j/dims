#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------
import csv
from io import StringIO

from hypothesis import given
from hypothesis import strategies as st
from pytest import MonkeyPatch
from structlog.testing import capture_logs

from dims.ingest import get_blob_data
from dims.ingest import get_blobs
from dims.ingest import storage

# --------------------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------------------


@st.composite
def random_csv(draw):
    """Create a random CSV file object using dicts."""
    dicts = draw(
        st.lists(
            st.dictionaries(
                keys=st.text(min_size=1), values=st.text(min_size=1), min_size=1
            ),
            min_size=1,
        )
    )
    fieldnames = []
    for d in dicts:
        fieldnames.extend(d.keys())
    csv_str = StringIO()
    writer = csv.DictWriter(csv_str, fieldnames=fieldnames, escapechar="\n")
    writer.writeheader()
    writer.writerows(dicts)
    csv_str.seek(0)
    return csv_str.read().encode()


def test_get_blobs(monkeypatch):
    """Test the get blobs functionality.

    We assume that Google has their stuff in order, and therefore we mock storage
    functionality in this test. Basically, we just test that our args are forwarded
    correctly.
    """
    monkeypatch.setattr(
        storage.Client,
        "list_blobs",
        lambda *args: args,
    )
    assert {"bucket", 32} <= set(get_blobs("bucket", 32))


@given(csv=random_csv(), blob_name=st.text())
def test_get_blob_data(csv, blob_name):
    """Use random csv file objects to check that we read blob data correctly.

    Because we generate csv-files with a minimum of one line, we expect empty data
    to be because of a parser error.
    """
    # Monkeypatch must be used as a context manager when using hypothesis.
    with MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(
            storage.Blob, "download_as_bytes", lambda *args, **kwargs: csv
        )
        blob = storage.Blob(blob_name, "test_bucket")
        with capture_logs() as log_output:
            blob_data = get_blob_data(blob)
            error = {
                "error": "line contains NUL",
                "event": "Failed to parse blob data",
                "log_level": "error",
            }
            if error in log_output:
                assert blob_data.data == []
            else:
                assert blob_data.data
                assert "timestamp" in blob_data.data[0].keys()
