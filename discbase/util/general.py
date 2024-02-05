import os
import random
import string
from pathlib import Path
from urllib.parse import urlparse

from discbase.enumeration.URLType import URLType

# TODO: test these


def get_random_string(length: int) -> str:
    if length < 1:
        raise Exception("Length must be greater than or equal to 1.")
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def get_file_extension(file_path: str) -> str:
    """
    Takes a path of a file and returns the extension with a "."
    "foo/bar.png" -> ".png"
    """
    extension = Path(file_path).suffix
    if extension == "":
        raise Exception("No file extension found.")
    return extension


def get_url_type(url: str) -> URLType:
    parsed = urlparse(url)
    if parsed.scheme in ["http", "https"]:
        return URLType.ONLINE
    elif os.path.exists(url):
        return URLType.LOCAL
    else:
        return URLType.UNKNOWN
