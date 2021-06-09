"""The data loading module.

This module provides functionalities to load data from S3 with specified columns and combine
DataFrames while filtering data by date.

"""

import logging

from src.s3 import download_to_pandas

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def read_data(s3path, columns):
    """Read data from S3 and select specified columns.

    Args:
        s3path (str): The S3 path that points to the file.
        columns (:obj:`list` of :obj:`str`): Names of the columns to use.

    Returns:
        :py:class:`pandas.DataFrame`: The data read into a DataFrame object.

    """
    # Read into dataframe
    df = download_to_pandas(s3path)

    # Select columns
    df = df[columns]

    return df


def combine_data(df1, df2, columns, date_col, start_date, end_date):
    """Combine DataFrames and filter by date.

    Args:
        df1 (:py:class:`pandas.DataFrame`): First DataFrame.
        df2 (:py:class:`pandas.DataFrame`): Second DataFrame.
        columns (:obj:`list` of :obj:`str`): The column names to use.
        date_col (str): Name of the column with date information.
        start_date (str): The start date (inclusive) of the final output data.
        end_date (str): The end date (exclusive) of the final output data.

    Returns:
        :py:class:`pandas.DataFrame`: The combined data as a DataFrame object.

    """
    # Rename columns
    df1.columns = columns
    df2.columns = columns

    # Append dataframes
    df = df1.append(df2)

    # Select subset by date
    df = df.loc[(df[date_col] >= start_date) & (df[date_col] < end_date)]
    df.drop(date_col, axis=1)
    df.reset_index(drop=True, inplace=True)

    logger.info("Successfully combined DataFrames")
    return df
