import pandas as pd
import pytest

from src import process


def test_remove_urls():
    input_str = "www.URL.com"
    output_true = " "
    output_test = process.remove_urls(input_str)
    assert output_true == output_test


def test_remove_urls_non_str():
    input_str = 123.456
    with pytest.raises(TypeError):
        process.remove_urls(input_str)


def test_remove_punctuations():
    input_str = ",.!?"
    output_true = "    "
    output_test = process.remove_punctuations(input_str)
    assert output_true == output_test


def test_remove_punctuations_non_str():
    input_str = 123.456
    with pytest.raises(TypeError):
        process.remove_punctuations(input_str)


def test_remove_stopwords():
    input_str = "This is a unit test"
    output_true = ['unit', 'test']
    output_test = process.remove_stopwords(input_str, "data/external/nltk_data")
    assert output_true == output_test


def test_remove_stopwords_non_str():
    input_str = 123.456
    with pytest.raises(AttributeError):
        process.remove_stopwords(input_str, "data/external/nltk_data")


def test_lemmatize():
    input_lst = ['tests']
    output_true = 'test'
    output_test = process.lemmatize(input_lst)
    assert output_true == output_test


def test_lemmatize_wrong_type():
    input_str = 123.456
    with pytest.raises(TypeError):
        process.lemmatize(input_str)


def test_process_tweet():
    input_str = "This is a unit test"
    output_true = "unit test"
    output_test = process.process_tweet(input_str, "data/external/nltk_data")
    assert output_true == output_test


def test_process_tweet_non_str():
    input_str = 123.456
    with pytest.raises(TypeError):
        process.process_tweet(input_str, "data/external/nltk_data")


def test_process_data():
    df_in = pd.DataFrame(["This is a unit test!", "This is a unit test too:)"],
                         columns=["content"])
    df_true = pd.DataFrame(["unit test", "unit test"], columns=["content"])
    df_test = process.process_data(df_in, "content", "data/external/nltk_data")
    pd.testing.assert_frame_equal(df_test, df_true)


def test_process_data_wrong_type():
    df_in = pd.DataFrame([1, 2], columns=["content"])
    with pytest.raises(TypeError):
        process.process_data(df_in, "content", "data/external/nltk_data")
