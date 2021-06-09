import pandas as pd
import numpy as np
import pytest

from src import model


def test_train_test_split():
    """Happy path for the train_test_split function."""
    # Define input dataframe
    df_in = pd.DataFrame(
        [['a', 1],
         ['b', 2],
         ['c', 3],
         ['d', 4],
         ['e', 5]], columns=['content', 'retweets'])

    # Define true outcome tuple
    train_contents = np.array(['c', 'e', 'd', 'b'])
    test_contents = np.array(['a'])
    train_labels = np.array([3, 5, 4, 2])
    test_labels = np.array([1])
    true_output = (train_contents, test_contents, train_labels, test_labels)

    # Get test outcome
    test_output = model.train_test_split(df_in, content_column="content", label_column="retweets",
                                         test_size=0.2, random_state=2021423)

    # Make sure tuples have the same length
    assert len(true_output) == len(test_output)

    # Make arrays in the tuples are the same
    assert all([np.array_equal(test, true) for test, true in zip(test_output, true_output)])


def test_train_test_split_non_df():
    """Unhappy path for the train_test_split function."""
    df_in = "Not a dataframe"
    with pytest.raises(AttributeError):
        model.train_test_split(df_in, content_column="content", label_column="retweets",
                               test_size=0.2, random_state=2021423)
