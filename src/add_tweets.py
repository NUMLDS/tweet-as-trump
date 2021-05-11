import logging.config

import sqlalchemy
from sqlalchemy import Column, BigInteger, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Tweets(Base):
    """Create a data model for the database to be set up for storing tweets."""
    __tablename__ = 'tweets'

    id = Column(String(64), primary_key=True)
    date = Column(DateTime, unique=False, nullable=False)
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
