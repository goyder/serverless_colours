import unittest
import json

from . import example_messages
import src.handler.handler as handler


class TestHandler(unittest.TestCase):

    def test_returns_bucket_and_key(self):
        """
        Pass in a typical s3 event and get the key and bucket back.
        :return:
        """
        response = handler.new_image(example_messages.example_message, "")
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

