"""
Generate utility functions associated with the Lambdas.
"""


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