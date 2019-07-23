"""
Generate utility functions associated with the Lambdas.
"""
from urllib.parse import urlparse


def generate_sourceref(key, bucket):
    """
    Combine a key and a bucket into a sourceref.
    :param key: String for a key.
    :param bucket: String of a bucket.
    :return: String of a sourceref.
    """
    if key[0] == "/":
        key = key[1:]

    return "s3://" + bucket + "/" + key


def get_bucket_and_key(s3uri):
    """
    Extract a key and a bucket from an s3 URI.
    :param s3uri:
    :return: Tuple of (bucket, key)
    """
    parsed_url = urlparse(s3uri)
    return parsed_url.netloc, parsed_url.path[1:]

