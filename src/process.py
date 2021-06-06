import logging
import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def remove_urls(input_str):
    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|" \
                r"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    output_str = re.sub(url_regex, " ", input_str)
    return output_str


def remove_punctuations(input_str):
    punctuation_regex = r"[^\w]"
    output_str = re.sub(punctuation_regex, " ", input_str)
    return output_str


def download_nltk_data(path):
    nltk.download("wordnet", download_dir=path)
    nltk.download("stopwords", download_dir=path)


def remove_stopwords(input_str):
    # Specify path to nltk data
    nltk.data.path.append("data/external/nltk_data")

    # Turn input str into lowercase
    lowercase = input_str.lower()

    # Split input str into list of words
    word_lst = lowercase.split()

    # Remove stopwords
    output_lst = [word for word in word_lst if word not in set(stopwords.words("english"))]

    return output_lst


def lemmatize(input_lst):
    lem = WordNetLemmatizer()
    lemmatized = [lem.lemmatize(word) for word in input_lst]

    # Join the list of words into a str
    result = " ".join(lemmatized)
    return result


def process_tweet(content):
    logger.debug("Processing the tweet with the following content: %s", content)

    # Remove URLs
    url_removed = remove_urls(content)
    logger.debug("Removed URL from the tweet: %s", url_removed)

    # Remove punctuations
    punctuation_removed = remove_punctuations(url_removed)
    logger.debug("Removed punctuations from the tweet: %s", punctuation_removed)

    # Remove stopwords
    stopwords_removed = remove_stopwords(punctuation_removed)
    logger.debug("Removed stopwords from the tweet: %s", stopwords_removed)

    # Lemmatize
    result = lemmatize(stopwords_removed)
    logger.debug("Lemmatized the tweet and this is the final result: %s", result)

    return result


def process_data(df, content_column):
    # Apply the function above to process all the tweets
    logger.info("Processing %s tweet contents. This may take a while.", len(df))
    df[content_column] = df[content_column].apply(process_tweet)
    logger.info("Successfully processed all the tweets")
    return df
