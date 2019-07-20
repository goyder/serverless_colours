import unittest
import os
from PIL import Image

from src.colours import colours

directory_name = os.path.dirname(os.path.realpath(__file__))
garfield_image_path = os.path.join(directory_name, "test_images", "atgarfield.jpg")


class TestImages(unittest.TestCase):

    def test_get_dimensions(self):
        """
        Test that we can pass the colours.image_dimensions functions a PIL image and get the dimensions back.
        :return:
        """
        garfield_img = Image.open(garfield_image_path)
        height = garfield_img.height
        width = garfield_img.width

        response = colours.get_dimensions(garfield_img)

        self.assertEqual(
            response["height"],
            height,
            "Height did not match as expected."
        )

        self.assertEqual(
            response["width"],
            width,
            "Width did not match as expected."
        )
