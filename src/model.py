import logging

import numpy as np
import pickle5 as pickle
import tensorflow as tf
from sklearn import model_selection
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def train_test_split(df, content_column, label_column, test_size, random_state):
    # Random shuffle to get random validation set in model fitting step
    df = df.sample(frac=1, random_state=random_state).reset_index(drop=True)

    # Get contents and labels
    contents = np.array(df[content_column])
    labels = np.array(df[label_column])

    # Train-test split
    train_contents, test_contents, train_labels, test_labels = model_selection.train_test_split(
        contents, labels, test_size=test_size, random_state=random_state)

    logger.info("Successfully split dataset into %s training samples and %s test samples",
                len(train_labels), len(test_labels))
    return train_contents, test_contents, train_labels, test_labels


def fit_tokenizer(train_contents, oov_token, tokenizer_path):
    # Fit tokenizer
    tokenizer = Tokenizer(oov_token=oov_token)
    tokenizer.fit_on_texts(train_contents)
    logger.info("Successfully trained tokenizer")

    # Save tokenizer
    with open(tokenizer_path, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    logger.info("Tokenizer saved to %s", tokenizer_path)

    # Calculate vocab size
    vocab_size = len(tokenizer.word_index) + 1
    logger.info("Vocabulary size calculated")
    return vocab_size


def tokenize(contents, tokenizer_path, padding_type, max_length):
    # Load tokenizer
    with open(tokenizer_path, 'rb') as handle:
        tokenizer = pickle.load(handle)
    logger.info("Successfully loaded tokenizer from %s", tokenizer_path)

    # Transform contents to sequences
    sequences = tokenizer.texts_to_sequences(contents)

    # Pad sequences
    result = pad_sequences(sequences, padding=padding_type, maxlen=max_length)
    logger.info("Successfully tokenized tweet content")
    return result


def compile_model(vocab_size, embedding_params, lstm_params, dense_params, output_params, dropout, compile_params):
    # Define model
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=vocab_size, **embedding_params),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(**lstm_params)),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(**dense_params),
        tf.keras.layers.Dropout(dropout),
        tf.keras.layers.Dense(**output_params)
    ])

    # Compile model
    model.compile(**compile_params)
    logger.info("Model compiled")
    return model


def fit_model(model, train_data, train_labels, epochs, verbose, validation_split, model_path):
    logger.info("Fitting neural network model")
    model.fit(train_data, train_labels, epochs=epochs, verbose=verbose, validation_split=validation_split)
    model.save(model_path)
    logger.info("Training complete! Model saved to %s", model_path)


def calculate_mape(model, test_data, test_labels):
    logger.info("Calculating predictions using %s test samples", len(test_labels))
    pred = np.round(model.predict(test_data))
    mape = np.mean(abs(pred - test_labels) / test_labels) * 100
    logger.info("Test MAPE: " + str(mape))
    return mape
