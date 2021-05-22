import argparse
import logging.config

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.s3 import upload_file_to_s3
from src.add_tweets import TweetManager, create_db

logging.config.fileConfig('config/logging/local.conf', disable_existing_loggers=False)
logger = logging.getLogger('trump-tweets-pipeline')


if __name__ == '__main__':
    # Add parsers for creating a database and adding tweets to it
    parser = argparse.ArgumentParser(description='Create database or upload data to s3')
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for uploading data to s3
    sb_upload = subparsers.add_parser('upload_data', description='Add data to s3 bucket')
    sb_upload.add_argument('--s3path', default='s3://2021-msia423-yu-dian/realdonaldtrump.csv',
                           help='s3 file path to upload data')
    sb_upload.add_argument('--local_path', default='data/raw/realdonaldtrump.csv',
                           help='local file path where the data is stored')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser('create_db', description='Create database')
    sb_create.add_argument('--engine_string', default=SQLALCHEMY_DATABASE_URI,
                           help='SQLAlchemy connection URI for database')

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser('ingest', description='Add data to database')
    sb_ingest.add_argument('--id', help='ID of tweet being added')
    sb_ingest.add_argument('--date', help='Date of tweet being added')
    sb_ingest.add_argument('--content', help='Content of tweet being added')
    sb_ingest.add_argument('--retweets', help='Number of retweets of tweet being added')
    sb_ingest.add_argument('--engine_string', default=SQLALCHEMY_DATABASE_URI,
                           help='SQLAlchemy connection URI for database')

    # Interpret and execute commands
    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == 'upload_data':
        upload_file_to_s3(args.local_path, args.s3path)
    elif sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        tm = TweetManager(engine_string=args.engine_string)
        tm.add_tweet(args.id, args.date, args.content, args.retweets)
        tm.close()
    else:
        parser.print_help()
