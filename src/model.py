import logging
import random

import yaml
import numpy as np
import pickle5 as pickle
import tensorflow as tf
from sklearn import model_selection
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow.keras.backend as K

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def set_seed(random_seed):
    # Set random seeds
    random.seed(random_seed)
    np.random.seed(random_seed)
    tf.random.set_seed(random_seed)
    session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
    sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
    K.set_session(sess)


def train_test_split(df, content_column, label_column, test_size, random_state):
    """Split data into training and test sets.

    Args:
        df (:py:class:`pandas.DataFrame`): Input data as a DataFrame object.
        content_column (str): The column name of the predictor content column.
        label_column (str): The column name of the target/response variable.
        test_size (float or int): The proportion of the dataset to include in the test split.
        random_state (int): Pass an int for reproducible output.

    Returns:
        :obj:`tuple` of :py:class:`numpy.array`: A tuple of training contents, test contents, training targets, and
        test targets as numpy arrays.

    """
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
    """Fit a tokenizer using training contents.

    Args:
        train_contents (:py:class:`numpy.array`): The training texts as a numpy array.
        oov_token (str): Token to replace out-of-vocabulary words.
        tokenizer_path (str): Path the save the trained tokenizer.

    Returns:
        int: The vocabulary size of the trained tokenizer.

    """
    # Fit tokenizer
    tokenizer = Tokenizer(oov_token=oov_token)
    tokenizer.fit_on_texts(train_contents)
    logger.info("Successfully trained tokenizer")

    # Save tokenizer
    try:
        with open(tokenizer_path, 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info("Tokenizer saved to %s", tokenizer_path)
    except Exception as e:
        logger.error("Unable to save tokenizer. Here is the original error: %s", e)

    # Calculate vocab size
    vocab_size = len(tokenizer.word_index) + 1
    logger.info("Vocabulary size calculated")
    return vocab_size


def tokenize(contents, tokenizer_path, padding_type, max_length):
    """Tokenize contents using a trained tokenizer.

    Args:
        contents (:py:class:`numpy.array`): The contents to tokenize as a pandas Series.
        tokenizer_path (str): The path that points to the trained tokenizer.
        padding_type (str): Pad either before ('pre') or after ('post') each sequence.
        max_length (int): Maximum length of all sequences.

    Returns:
        :py:class:`numpy.array` of :py:class:`numpy.array`: An array of arrays, in which each sub-array is the result
        of tokenizing and padding a input content.

    """
    # Load tokenizer
    try:
        with open(tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)
        logger.info("Successfully loaded tokenizer from %s", tokenizer_path)
    except FileNotFoundError:
        logger.error("Cannot find the specified tokenizer path %s", tokenizer_path)
    except Exception as e:
        logger.error("Unable to load tokenizer. Here is the original error: %s", e)

    # Transform contents to sequences
    sequences = tokenizer.texts_to_sequences(contents)

    # Pad sequences
    result = pad_sequences(sequences, padding=padding_type, maxlen=max_length)
    logger.info("Successfully tokenized tweet content")
    return result


def compile_model(vocab_size, embedding_params, lstm_params, dense_params, output_params, dropout, compile_params):
    """Specify the LSTM model architecture and compile the model.

    Args:
        vocab_size (int): The vocabulary size to use in the embedding layer. Calculated when fitting the tokenizer.
        embedding_params (dict): The parameters for the embedding layer (output_dim, input_length, etc.)
        lstm_params (dict): The parameters for the LSTM layer (units, return_sequences, recurrent_dropout, etc.)
        dense_params (dict): The parameters for the hidden dense layer (units, activation, etc.)
        output_params (dict): The parameters for the output layer (units, activation, etc.)
        dropout (float): Fraction of the input units to drop.
        compile_params (dict): The parameters for compiling the model (loss, optimizer, etc.)

    Returns:
        :py:class:`tf.keras.Model`: The compiled keras model object.

    """
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
    """Fit a keras model using provided training set.

    Args:
        model (:py:class:`tf.keras.Model`): A compiled keras model object.
        train_data (:py:class:`numpy.array`): The training data.
        train_labels (:py:class:`numpy.array`): The training labels.
        epochs (int): Number of iterations to train the model.
        verbose (int): Verbosity mode. 0 = silent, 1 = progress bar, 2 = one line per epoch.
        validation_split (float): Fraction of the training data to be used as validation data.
        model_path (str): Path to save the trained model.

    Returns:
        None

    """
    logger.info("Fitting neural network model")
    model.fit(train_data, train_labels, epochs=epochs, verbose=verbose, validation_split=validation_split)
    model.save(model_path)
    logger.info("Training complete! Model saved to %s", model_path)


def calculate_mape(test_data, test_labels, fitted_model_path, output_path):
    """Calculate the Mean Absolute Percentage Error (MAPE) of a trained model.

    Args:
        fitted_model_path (str): The path that points to a fitted model.
        test_data (:py:class:`numpy.array`): The test data.
        test_labels (:py:class:`numpy.array`): The test labels.
        output_path (str): The path to a yaml file to save the calculated MAPE.

    Returns:
        None

    """
    try:
        logger.info("Loading pre-trained model from %s", fitted_model_path)
        model = keras.models.load_model(fitted_model_path)
    except OSError:
        logger.error("Fitted model does not exist at the specified path %s", fitted_model_path)

    logger.info("Calculating predictions using %s test samples", len(test_labels))
    pred = np.round(model.predict(test_data))
    mape = np.mean(abs(pred - test_labels) / test_labels) * 100
    logger.info("Test MAPE: " + str(mape))

    mape_dict = {"mape": float(mape)}
    try:
        logger.info("Saving calculated result")
        with open(output_path, 'w') as f:
            yaml.dump(mape_dict, f)
    except Exception as e:
        logger.error("Unable to save result. Here is the original error: %s", e)
    logger.info("Result saved to %s", output_path)
