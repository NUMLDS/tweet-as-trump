"""The text processing module.

This module provides functionalities to process a single text or a column of texts within a
DataFrame.

"""

import logging
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def remove_urls(input_str):
    """Remove all URLs from the input text.

    Args:
        input_str (str): The input text.

    Returns:
        str: Output text with URLs removed.

    """
    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)" \
                r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|" \
                r"(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    output_str = re.sub(url_regex, " ", input_str)
    return output_str


def remove_punctuations(input_str):
    """Remove all punctuations from the input text.

    Args:
        input_str (str): The input text.

    Returns:
        str: Output text with punctuations removed.

    """
    punctuation_regex = r"[^\w]"
    output_str = re.sub(punctuation_regex, " ", input_str)
    return output_str


def remove_stopwords(input_str, nltk_data_path):
    """Remove all stopwords from the input text.

    Args:
        input_str (str): The input text.
        nltk_data_path (str): The path that points to the downloaded NLTK data.

    Returns:
        :obj:`list` of :obj:`str`: Output text as a list of words.

    """
    # Specify path to nltk data
    nltk.data.path.append(nltk_data_path)

    # Turn input str into lowercase
    lowercase = input_str.lower()

    # Split input str into list of words
    word_lst = lowercase.split()

    # Remove stopwords
    output_lst = [word for word in word_lst if word not in set(stopwords.words("english"))]

    return output_lst


def lemmatize(input_lst):
    """Apply lemmatization to each word in the input list.

    Args:
        input_lst (:obj:`list` of :obj:`str`): Input text as a list of words.

    Returns:
        str: Output text after lemmatization.

    """
    lem = WordNetLemmatizer()
    lemmatized = [lem.lemmatize(word) for word in input_lst]

    # Join the list of words into a str
    result = " ".join(lemmatized)
    return result


def download_nltk_data(nltk_data_path):
    """Download NLTK corpora data to specified path.

    Args:
        nltk_data_path (str): The path to download NLTK data to.

    Returns:
        None

    """
    try:
        logger.info("Downloading NLTK corpora data to %s", nltk_data_path)
        nltk.download("wordnet", download_dir=nltk_data_path)
        nltk.download("stopwords", download_dir=nltk_data_path)
        logger.info("Successfully downloaded nltk data")
    except Exception as e:
        logger.error("Unable to download NLTK data. Here is the original error: %s", e)


def process_tweet(content, nltk_data_path, download=False):
    """Apply all processing steps to a tweet.

    Args:
        content (str): Content of the tweet.
        nltk_data_path (str): The path that points to the downloaded NLTK data or where the data
        should be downloaded.
        download (bool): Whether to download NLTK data.

    Returns:
        str: Output text after all processing steps.

    """
    # Download nltk data if specified
    if download:
        download_nltk_data(nltk_data_path)

    logger.debug("Processing the tweet with the following content: %s", content)

    # Remove URLs
    url_removed = remove_urls(content)
    logger.debug("Removed URL from the tweet: %s", url_removed)

    # Remove punctuations
    punctuation_removed = remove_punctuations(url_removed)
    logger.debug("Removed punctuations from the tweet: %s", punctuation_removed)

    # Remove stopwords
    stopwords_removed = remove_stopwords(punctuation_removed, nltk_data_path)
    logger.debug("Removed stopwords from the tweet: %s", stopwords_removed)

    # Lemmatize
    result = lemmatize(stopwords_removed)
    logger.debug("Lemmatized the tweet and this is the final result: %s", result)

    return result


def process_data(df, content_column, nltk_data_path, download=False):
    """Process all texts in a DataFrame column.

    Args:
        df (:py:class:`pandas.DataFrame`): The DataFrame to process.
        content_column (str): The name of the content column.
        nltk_data_path (str): The path that points to the downloaded NLTK data or where the data
        should be downloaded.
        download (bool): Whether to download NLTK data.

    Returns:
        :py:class:`pandas.DataFrame`: The processed data as a DataFrame object.

    """
    # Download nltk data if specified
    if download:
        download_nltk_data(nltk_data_path)

    # Apply the function above to process all the tweets
    logger.info("Processing %s tweet contents. This may take a while.", len(df))
    df[content_column] = df[content_column].apply(process_tweet, nltk_data_path=nltk_data_path)
    logger.info("Successfully processed all the tweets")
    return df
