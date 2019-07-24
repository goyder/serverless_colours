import unittest
import unittest.mock as mock
import json

from . import example_messages
import src.handler.handler as handler
import src.handler.util as util


class TestListImages(unittest.TestCase):

    def test_returns_list_of_images(self):
        """
        Pass in a test bucket and get a list of images ready for crunching back.
        :return:
        """
        bucket_name = example_messages.bucket_location["bucket"]
        expected_keys = ["folder/image1.jpg", "image2.jpg"]
        handler.retrieve_images = mock.MagicMock(return_value=expected_keys)

        image_list = handler.list_images(example_messages.bucket_location, None)

        self.assertEqual(
            image_list['s3uris'][-1],
            "DONE",
            "Image list did not end with 'DONE' as required."
        )

        for key in expected_keys:
            s3uri = util.generate_sourceref(key, bucket_name)
            self.assertEqual(
                s3uri in image_list['s3uris'],
                True,
                "Did not find s3urt '{}' in image list.".format(s3uri)
            )


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

