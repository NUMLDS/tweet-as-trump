import pandas as pd
import pytest

from src import clean


def test_remove_outliers():
    df_in = pd.DataFrame([1, 2, 3, 4, 5], columns=["value"])
    df_true = pd.DataFrame([1, 2, 3], columns=["value"])
    df_test = clean.remove_outliers(df_in, "value", cutoff=4, left_tail=False)
    pd.testing.assert_frame_equal(df_test, df_true)


def test_remove_outliers_non_df():
    df_in = "Not a dataframe"
    with pytest.raises(AttributeError):
        clean.remove_outliers(df_in, "value", 2)


def test_drop_empty_content():
    df_in = pd.DataFrame(["a", "b", "c", "", ""], columns=["content"])
    df_true = pd.DataFrame(["a", "b", "c"], columns=["content"])
    df_test = clean.drop_empty_content(df_in, "content")
    pd.testing.assert_frame_equal(df_test, df_true)


def test_drop_empty_content_non_df():
    df_in = "Not a dataframe"
    with pytest.raises(TypeError):
        clean.drop_empty_content(df_in, "content")


def test_is_en():
    input_str = "This is English"
    assert clean.is_en(input_str)


def test_is_en_non_str():
    input_str = 123
    with pytest.raises(TypeError):
        clean.is_en(input_str)


def test_drop_non_en_content():
    df_in = pd.DataFrame(["a", "b", "c", "%", "!"], columns=["content"])
    df_true = pd.DataFrame(["a", "b", "c"], columns=["content"])
    df_test = clean.drop_non_en_content(df_in, "content")
    pd.testing.assert_frame_equal(df_test, df_true)


def test_drop_non_en_content_wrong_type():
    df_in = pd.DataFrame([1, 2, 3, 4, 5], columns=["content"])
    with pytest.raises(TypeError):
        clean.drop_non_en_content(df_in, "content")



