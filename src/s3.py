import argparse
import logging
import re

import boto3
import botocore

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("s3transfer").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("aiobotocore").setLevel(logging.ERROR)
logging.getLogger("s3fs").setLevel(logging.ERROR)


logger = logging.getLogger('s3')


def parse_s3(s3path):
    """
    Parse s3 path.
    Source: https://github.com/MSIA/2021-msia423/blob/main/aws-s3/s3.py
    """
    regex = r"s3://([\w._-]+)/([\w./_-]+)"

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path, s3path):
    """
    Upload the file in local path to s3
    Args:
        local_path (str): the path that points to the local data
        s3path (str): the s3 path that the data will be uploaded to
    Returns: None
    """

    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)


def download_file_from_s3(local_path, s3path):
    """
    Download a data file from s3
    Args:
        local_path (str): the path that will store the downloaded data
        s3path (str): the s3 path that the data will be downloaded from
    Returns: None
    """
    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(s3bucket)

    try:
        bucket.download_file(s3_just_path, local_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data downloaded from %s to %s', s3path, local_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--download', default=False, action='store_true',
                        help="If True, will download the data from S3. If False, will upload data to S3")
    parser.add_argument('--s3path', default='s3://2021-msia423-yu-dian/trump_tweets.csv',
                        help="s3 data path to download or upload data")
    parser.add_argument('--local_path', default='data/raw/trump_tweets.csv',
                        help="local data path to store or upload data")
    args = parser.parse_args()

    if args.download:
        download_file_from_s3(args.local_path, args.s3path)
    else:
        upload_file_to_s3(args.local_path, args.s3path)
