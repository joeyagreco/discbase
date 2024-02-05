from shutil import copyfileobj

import requests

# TODO: test these


def save_image_from_url(*, url: str, save_path: str) -> None:
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(save_path, "wb") as out_file:
        copyfileobj(response.raw, out_file)

    return save_path
