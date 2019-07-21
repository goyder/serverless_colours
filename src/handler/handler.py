import json
import logging
import boto3
import os
from PIL import Image

from src.colours import colours
from src.handler import util

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def new_image(event, context):
    """Accept a new image being created and log the information to file.
    :param event:
    :param context:
    :return:
    """
    s3_client = boto3.client("s3")
    ddb_resource = boto3.resource("dynamodb")
    table = ddb_resource.Table(os.environ["DYNAMODB_TABLE"])

    key = event["Records"][0]["s3"]["object"]["key"]
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    logger.info("Found new image in bucket '{}' with key '{}'.".format(
        bucket,
        key
    ))

    # We have to open the image provided.
    img = Image.open(s3_client.get_object(
        Key=key,
        Bucket=bucket,
    )['Body'])

    # We then get some data about it.
    dimensions = colours.get_dimensions(img)
    s3uri = util.generate_sourceref(key, bucket)

    body = {
        "s3uri": s3uri,
        "key": key,
        "bucket": bucket,
        "height": dimensions["height"],
        "width": dimensions["width"]
    }
    logger.info("Logging to dynamodb for image '{}'.".format(s3uri))

    table.put_item(
        Item={
            "sourceref": body["s3uri"],
            "key": key,
            "bucket": bucket,
            "height": dimensions["height"],
            "width": dimensions["width"]
        }
    )

    logger.info(body)
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
