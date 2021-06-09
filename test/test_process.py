import pandas as pd
import pytest

from src import process


def test_remove_urls():
    """Happy path for the remove_urls function."""
    input_str = "www.URL.com"
    output_true = " "
    output_test = process.remove_urls(input_str)
    assert output_true == output_test


def test_remove_urls_non_str():
    """Unhappy path for the remove_urls function."""
    input_str = 123.456
    with pytest.raises(TypeError):
        process.remove_urls(input_str)


def test_remove_punctuations():
    """Happy path for the remove_punctuations function."""
    input_str = ",.!?"
    output_true = "    "
    output_test = process.remove_punctuations(input_str)
    assert output_true == output_test


def test_remove_punctuations_non_str():
    """Unhappy path for the remove_punctuations function."""
    input_str = 123.456
    with pytest.raises(TypeError):
        process.remove_punctuations(input_str)


def test_remove_stopwords():
    """Happy path for the remove_stopwords function."""
    input_str = "This is a unit test"
    output_true = ['unit', 'test']
    output_test = process.remove_stopwords(input_str, "data/external/nltk_data")
    assert output_true == output_test


def test_remove_stopwords_non_str():
    """Unhappy path for the remove_stopwords function."""
    input_str = 123.456
    with pytest.raises(AttributeError):
        process.remove_stopwords(input_str, "data/external/nltk_data")


def test_lemmatize():
    """Happy path for the lemmatize function."""
    input_lst = ['tests']
    output_true = 'test'
    output_test = process.lemmatize(input_lst)
    assert output_true == output_test


def test_lemmatize_wrong_type():
    """Unhappy path for the lemmatize function."""
    input_str = 123.456
    with pytest.raises(TypeError):
        process.lemmatize(input_str)


def test_process_tweet():
    """Happy path for the process_tweet function (without network call)."""
    input_str = "This is a unit test"
    output_true = "unit test"
    output_test = process.process_tweet(input_str, "data/external/nltk_data")
    assert output_true == output_test


def test_process_tweet_non_str():
    """Unhappy path for the process_tweet function (without network call)."""
    input_str = 123.456
    with pytest.raises(TypeError):
        process.process_tweet(input_str, "data/external/nltk_data")


def test_process_data():
    """Happy path for the process_data function (without network call)."""
    df_in = pd.DataFrame(["This is a unit test!", "This is a unit test too:)"],
                         columns=["content"])
    df_true = pd.DataFrame(["unit test", "unit test"], columns=["content"])
    df_test = process.process_data(df_in, "content", "data/external/nltk_data")
    pd.testing.assert_frame_equal(df_test, df_true)


def test_process_data_wrong_type():
    """Unhappy path for the process_data function (without network call)."""
    df_in = pd.DataFrame([1, 2], columns=["content"])
    with pytest.raises(TypeError):
        process.process_data(df_in, "content", "data/external/nltk_data")
