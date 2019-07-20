import json
import logging
from src import colours

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def new_image(event, context):
    # Accept a new image being created and log the information to file.
    key = event["Records"][0]["s3"]["object"]["key"]
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    logger.info("Found new image in bucket '{}' with key '{}'.".format(
        bucket,
        key
    ))

    body = {
        "key": key,
        "bucket": bucket
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
