import logging.config

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Tweets(Base):
    """Create a data model for the database to be set up for storing tweets."""
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True)
    content = Column(String(280), unique=False, nullable=False)
    retweets = Column(BigInteger, unique=False, nullable=False)

    def __repr__(self):
        return '<Tweet id %r>' % id


def create_db(engine_string):
    """Create database from provided engine string.

    Args:
        engine_string (str): Engine string.

    Returns:
        None

    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")


class TweetManager:

    def __init__(self, app=None, engine_string=None):
        """Initialize a TweetManager object.

        Args:
            app (Flask): Flask app.
            engine_string (str): Engine string.

        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self):
        """Close session.

        Returns:
            None

        """
        self.session.close()

    def add_tweet(self, content, retweets):
        """Seed an existing database with additional tweets.

        Args:
            content (str): Content of the tweet
            retweets (str): Number of retweets as a String

        Returns:
            None

        """
        session = self.session
        tweet = Tweets(content=content, retweets=retweets)
        session.add(tweet)
        session.commit()
        logger.info("Successfully added tweet to database.")
