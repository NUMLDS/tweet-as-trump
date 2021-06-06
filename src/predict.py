from tensorflow import keras

from src.model import tokenize
from src.process import process_tweet


def predict(input_tweet, tokenizer_path, padding_type, max_length, fitted_model):
    processed = process_tweet(input_tweet)
    tokenized = tokenize([processed], tokenizer_path, padding_type, max_length)
    model = keras.models.load_model(fitted_model)
    prediction = round(model.predict(tokenized)[0][0])
    return prediction
