import logging

from tensorflow import keras

from src.model import tokenize
from src.process import process_tweet

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def predict(input_tweet, nltk_data_path, tokenizer_path, padding_type, max_length, fitted_model_path):
    """Predict number of retweets using a pre-trained model.

    Args:
        input_tweet (str): The input tweet.
        nltk_data_path (str): The path that points to the downloaded NLTK data.
        tokenizer_path (str): The path that points to a trained tokenizer.
        padding_type (str): Pad either before ('pre') or after ('post') each sequence.
        max_length (int): Maximum length of all sequences.
        fitted_model_path (str): The path that points to a trained model.

    Returns:
        int: The predicted number of retweets.

    """
    # Process
    processed = process_tweet(input_tweet, nltk_data_path)
    logger.info("Input tweet processed.")

    # Tokenize
    tokenized = tokenize([processed], tokenizer_path, padding_type, max_length)

    # Load fitted model
    try:
        logger.info("Loading pre-trained model from %s", fitted_model_path)
        model = keras.models.load_model(fitted_model_path)
    except OSError:
        logger.error("Fitted model does not exist at the specified path %s", fitted_model_path)

    # Calculate prediction
    logger.info("Calculating predictions.")
    prediction = round(model.predict(tokenized)[0][0])
    logger.info("The predicted number of retweets is %s", prediction)
    return prediction
