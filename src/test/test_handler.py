import unittest
import json

from . import example_messages
import src.handler.handler as handler
import src.handler.util as util


class TestHandler(unittest.TestCase):

    def test_returns_bucket_and_key(self):
        """
        Pass in a typical s3 event and get the key and bucket back.
        :return:
        """
        response = handler.new_image(example_messages.s3_object_location, "")
        body = json.loads(response["body"])

        self.assertEqual(
            body["key"],
            "HappyFace.jpg",
            "Key did not match as expected."
        )

        self.assertEqual(
            body["bucket"],
            "sourcebucket",
            "Bucket did not match as expected."
        )


class TestUtil(unittest.TestCase):
    """
    Tests associated with the util module.
    """

    def test_s3uri_returned(self):
        """
        If we return a standard bucket and key, we should get a usable s3 URI in return.
        :return:
        """
        key = "hello/mate"
        bucket = "databucket"
        s3_uri = "s3://databucket/hello/mate"

        self.assertEqual(
            util.generate_sourceref(key, bucket),
            s3_uri,
            "Returned s3 URI did not match as expected."
        )

    def test_s3_uri_returned_with_leading_slash(self):
        """
        If we return a standard bucket but the key has a leading slash, we should get a usable s3 URI in return.
        :return:
        """
        key = "/hello/mate"
        bucket = "databucket"
        s3_uri = "s3://databucket/hello/mate"

        self.assertEqual(
            util.generate_sourceref(key, bucket),
            s3_uri,
            "Returned s3 URI did not match as expected."
        )

    def test_get_key_and_bucket_from_s3_uri(self):
        """
        If we pass in an s3 URI, get the key and bucket back.
        :return:
        """
        s3uri = "s3://databucket/hello/mate"
        bucket, key = util.get_bucket_and_key(s3uri)

        self.assertEqual(
            "databucket",
            bucket,
            "Bucket did not match as expected."
        )

        self.assertEqual(
            "hello/mate",
            key,
            "Key did not match as expected."
        )

