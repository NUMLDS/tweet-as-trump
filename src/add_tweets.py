import logging.config

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, DateTime, String
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Tweets(Base):
    """
    Create a data model for the database to be set up for storing Trump's tweets
    """

    __tablename__ = 'tweets'

    id = Column(String(64), primary_key=True)
    date = Column(DateTime, unique=False, nullable=False)
    content = Column(String(280), unique=False, nullable=False)
    retweets = Column(BigInteger, unique=False, nullable=False)

    def __repr__(self):
        return '<Tweet id %r>' % id


def create_db(engine_string):
    """Create database from provided engine string

    Args:
        engine_string: str - Engine string

    Returns: None

    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")


class TweetManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app: Flask - Flask app
            engine_string: str - Engine string
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
        """
        Closes session.

        Returns: None

        """
        self.session.close()

    def add_tweet(self, id, date, content, retweets):
        """
        Seeds an existing database with additional tweets.
        Args:
            id (string): Tweet id
            date (str): date of the tweet
            content (str): content of the tweet
            retweets (int): number of retweets
        Returns: None
        """
        session = self.session
        content = Tweets(id=id, date=date, content=content, retweets=retweets)
        session.add(content)
        session.commit()
        logger.info("Tweet with id %s, added to database", id)
