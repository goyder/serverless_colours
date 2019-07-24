import json
import logging
import boto3
import os
from PIL import Image

from src.colours import colours
from src.handler import util

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def retrieve_images(bucket_name):
    """
    Retrieve all images from a bucket. Filters purely by whether suffix is .jpg.
    :param bucket: String of a bucket name.
    :return: List of images in a bucket in the form of ['key1', 'key2', 'key3'...]
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    items = [item.key for item in bucket.objects.all() if str(item.key)[-4:] == ".jpg"]
    return items


def list_images(event, context):
    """
    Accept an s3 location and return all images within it.
    :param event: Input from StateFunction. Should be in format {'bucket': 'bucketname'}.
    :param context:
    :return: Returns {"s3uris": ["s3://bucket/key1", "s3://bucket/key2", "DONE"] }'
    """
    bucket_name = event['bucket']
    images = retrieve_images(bucket_name)

    # Retrieve the relevant location.
    s3uris = [util.generate_sourceref(key, bucket_name) for key in images]

    # Ship it!
    s3uris.append("DONE")
    response = {
        "s3uris": s3uris
    }
    return response


def new_image(event, context):
    """Accept a new image being created and log the information to file.
    :param event:
    :param context:
    :return:
    """
    s3_client = boto3.client("s3")

    s3uri = event["s3uri"]
    bucket, key = util.get_bucket_and_key(s3uri)
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
        "height": str(dimensions["height"]),
        "width": str(dimensions["width"])
    }

    logger.info(body)
    response = {
        "statusCode": 200,
        "body": body
    }

    return response
