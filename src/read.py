import logging

from src.s3 import download_to_pandas

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def read_data(s3path, columns):
    # Read into dataframe
    df = download_to_pandas(s3path)

    # Select columns
    df = df[columns]

    return df


def combine_data(df1, df2, columns, date_col, start_date, end_date):
    # Rename columns
    df1.columns = columns
    df2.columns = columns

    # Append dataframes
    df = df1.append(df2)

    # Select subset by date
    df = df.loc[(df[date_col] >= start_date) & (df[date_col] < end_date)]
    df.drop(date_col, axis=1)

    logger.info("Successfully combined DataFrames")
    return df
