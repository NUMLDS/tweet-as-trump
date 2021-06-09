import pytest

from src import s3


def test_parse_s3():
    """Happy path for the parse_s3 function."""
    s3path_in = "s3://test_bucket/test_file.csv"
    tuple_true = ("test_bucket", "test_file.csv")
    tuple_test = s3.parse_s3(s3path_in)
    assert tuple_test == tuple_true


def test_parse_s3_invalid_path():
    """Happy path for the parse_s3 function."""
    # Pass in a invalid s3 path
    s3path_in = "invalid/path"
    with pytest.raises(AttributeError):
        s3.parse_s3(s3path_in)
