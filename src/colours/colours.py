def get_dimensions(img):
    """
    Return the dimensions of a PIL image.
    :param img: A PIL image.
    :return: Dictionary with height and width.
    """
    return {
        "height": img.height,
        "width": img.width
    }
