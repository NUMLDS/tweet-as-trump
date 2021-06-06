import logging
import re

import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def remove_outliers(df, column, cutoff, left_tail=True):
    if left_tail:
        df = df.loc[df[column] > cutoff].copy()
    else:
        df = df.loc[df[column] < cutoff].copy()
    logger.info("Removed outliers")
    return df


def drop_empty_content(df, content_column):
    df[content_column].replace('', np.nan, inplace=True)
    df.dropna(inplace=True)
    logger.info("Dropped tweets with empty content")
    return df


def is_en(text):
    en_regex = re.compile(r'[a-zA-Z1-9]')
    match = en_regex.match(text)
    if match:
        return True
    else:
        return False


def drop_non_en_content(df, content_column):
    df = df[df[content_column].apply(is_en)]
    logger.info("Dropped non-English tweets")
    return df
