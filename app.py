"""Flask wrapper for running the model.

This script defines how the web application works and renders HTML templates.

"""

import logging.config

import yaml
from flask import Flask
from flask import render_template, request

from src.add_tweets import TweetManager
from src.predict import predict

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
tweet_manager = TweetManager(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Index page for user to input text."""
    logger.info("Index page rendered.")
    return render_template('index.html')


@app.route('/tweet', methods=['POST'])
def tweet():
    """Collect user input, calculate prediction, and persist data to database."""
    # Get user input
    tweet_content = request.form['tweet_content']
    logger.info("User input is '%s'", tweet_content)

    # Load model configuration file
    try:
        with open(app.config["MODEL_CONFIG"], "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logger.info("Configuration file loaded from %s", app.config["MODEL_CONFIG"])
    except FileNotFoundError:
        logger.error("Cannot find configuration file from the path: %s", app.config["MODEL_CONFIG"])

    # Calculate prediction
    prediction = predict(tweet_content, **config["predict"]["predict"])

    # Save user input and predicted retweets to database
    try:
        tweet_manager.add_tweet(content=tweet_content, retweets=prediction)
        return render_template('tweet.html', tweet_content=tweet_content, prediction=prediction)
    except Exception as e:
        logger.warning("Unable to add to database, error page returned. "
                       "Here is the original error: %s", e)
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
