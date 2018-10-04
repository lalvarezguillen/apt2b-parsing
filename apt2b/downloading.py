import os
import requests
import retry
from .config import IMAGES_FOLDER


class RetriableHTTPError(Exception):
    """
    Raised when we get an HTTP error code that's worth retrying
    """


RETRIABLE_CODES = [429] + list(range(500, 600))


class FatalHTTPError(Exception):
    """
    Raised when we get an HTTP error code that's not worth retrying.
    """


FATAL_CODES = list(range(400, 500))

OK_CODES = list(range(200, 300))


@retry.retry(exceptions=(RetriableHTTPError,), tries=3, backoff=5, delay=5)
def download_image(filename: str, url: str):
    """
    Downloads an image from its URL, and stores it the directory selected
    for that purpose.

    Args:
        url: The URL where the image is hosted
        filename: The filename of the image.
    """
    resp = requests.get(url)

    if resp.status_code in OK_CODES:
        filepath = os.path.join(IMAGES_FOLDER, filename)
        with open(filepath, "wb") as imgfile:
            imgfile.write(resp.content)
        return

    print(resp.status_code, url)
    if resp.status_code in RETRIABLE_CODES:
        raise RetriableHTTPError

    if resp.status_code in FATAL_CODES:
        raise FatalHTTPError
