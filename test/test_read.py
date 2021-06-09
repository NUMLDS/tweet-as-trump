import pandas as pd
import pytest

from src import read


def test_combine_data():
    df1 = pd.DataFrame(
        [['2020-01-01', 'a', 1],
         ['2020-01-02', 'b', 2],
         ['2020-01-03', 'c', 3],
         ['2020-01-04', 'd', 4],
         ['2020-01-05', 'e', 5]], columns=['date', 'content', 'retweets'])

    df2 = pd.DataFrame(
        [['2020-01-06', 'f', 6],
         ['2020-01-07', 'g', 7],
         ['2020-01-08', 'h', 8],
         ['2020-01-09', 'i', 9],
         ['2020-01-10', 'j', 0]], columns=['date', 'text', 'num'])

    df_true = pd.DataFrame(
        [['2020-01-05', 'e', 5],
         ['2020-01-06', 'f', 6],
         ['2020-01-07', 'g', 7]], columns=['date', 'content', 'retweets']
    )

    df_test = read.combine_data(df1, df2, columns=['date', 'content', 'retweets'], date_col="date",
                                start_date="2020-01-05", end_date="2020-01-08")

    pd.testing.assert_frame_equal(df_test, df_true)


def test_combine_data():
    df1 = pd.DataFrame(
        [['2020-01-01', 'a', 1],
         ['2020-01-02', 'b', 2],
         ['2020-01-03', 'c', 3],
         ['2020-01-04', 'd', 4],
         ['2020-01-05', 'e', 5]], columns=['date', 'content', 'retweets'])

    df2 = pd.DataFrame(
        [['2020-01-06', 'f', 6],
         ['2020-01-07', 'g', 7],
         ['2020-01-08', 'h', 8],
         ['2020-01-09', 'i', 9],
         ['2020-01-10', 'j', 0]], columns=['date', 'text', 'num'])

    df_true = pd.DataFrame(
        [['2020-01-05', 'e', 5],
         ['2020-01-06', 'f', 6],
         ['2020-01-07', 'g', 7]], columns=['date', 'content', 'retweets']
    )

    df_test = read.combine_data(df1, df2, columns=['date', 'content', 'retweets'], date_col="date",
                                start_date="2020-01-05", end_date="2020-01-08")

    pd.testing.assert_frame_equal(df_test, df_true)


def test_combine_data_non_df():
    df1 = [['2020-01-01', 'a', 1],
           ['2020-01-02', 'b', 2],
           ['2020-01-03', 'c', 3],
           ['2020-01-04', 'd', 4],
           ['2020-01-05', 'e', 5]]

    df2 = [['2020-01-06', 'f', 6],
           ['2020-01-07', 'g', 7],
           ['2020-01-08', 'h', 8],
           ['2020-01-09', 'i', 9],
           ['2020-01-10', 'j', 0]]

    with pytest.raises(AttributeError):
        read.combine_data(df1, df2, columns=['date', 'content', 'retweets'], date_col="date",
                          start_date="2020-01-05", end_date="2020-01-08")
