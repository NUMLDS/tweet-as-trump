import logging
import re

import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def remove_outliers(df, column, cutoff, left_tail=True):
    """Remove outliers based on conditions specified.

    Args:
        df (:py:class:`pandas.DataFrame`): The DataFrame to remove outliers from.
        column (str): Name of the column that contains outliers.
        cutoff (int/float): A number as a cutoff for outliers.
        left_tail (bool): If True, remove the left tail of the distribution. Otherwise, remove the right tail.

    Returns:
        :py:class:`pandas.DataFrame`: The DataFrame after removing outliers.

    """
    if left_tail:
        df = df.loc[df[column] > cutoff].copy()
    else:
        df = df.loc[df[column] < cutoff].copy()
    logger.info("Removed outliers")
    return df


def drop_empty_content(df, content_column):
    """Drop rows with an empty string in the specified column.

    Args:
        df (:py:class:`pandas.DataFrame`): The DataFrame to use.
        content_column (str): Name of the column to detect empty contents.

    Returns:
        :py:class:`pandas.DataFrame`: The DataFrame after dropping empty contents.

    """
    df[content_column].replace('', np.nan, inplace=True)
    df.dropna(inplace=True)
    logger.info("Dropped tweets with empty content")
    return df


def is_en(text):
    """Helper function to check whether the input text only contains letters and numbers.

    Args:
        text (str): The input text.

    Returns:
        bool: Whether or not the input text is English (contains only letters and numbers).

    """
    en_regex = re.compile(r'[a-zA-Z1-9]')
    match = en_regex.match(text)
    if match:
        return True
    else:
        return False


def drop_non_en_content(df, content_column):
    """Drop all rows that contain non-English content.

    Args:
        df (:py:class:`pandas.DataFrame`): The DataFrame to use.
        content_column (str): Name of the content column.

    Returns:
        :py:class:`pandas.DataFrame`: The DataFrame after dropping non-English contents.

    """
    df = df[df[content_column].apply(is_en)]
    logger.info("Dropped non-English tweets")
    return df
