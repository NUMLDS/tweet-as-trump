import argparse
import logging.config

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('trump-tweets-pipeline')

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.add_tweets import TweetManager, create_db


if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--id", help="ID of tweet being added")
    sb_ingest.add_argument("--date", help="Date of tweet being added")
    sb_ingest.add_argument("--content", help="Content of tweet being added")
    sb_ingest.add_argument("--retweets", help="Number of retweets of tweet being added")
    sb_ingest.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        tm = TweetManager(engine_string=args.engine_string)
        tm.add_tweet(args.id, args.date, args.content, args.retweets)
        tm.close()
    else:
        parser.print_help()



