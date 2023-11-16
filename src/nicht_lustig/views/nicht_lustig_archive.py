import itertools
import json
import random
import re
from typing import List

import requests
from bs4 import BeautifulSoup

from flask import current_app, Blueprint, render_template
from flask_caching import Cache

BASE_URL = "https://joscha.com/nichtlustig"
MEDIA_URL = "https://joscha.com/data/media/cartoons/"
IMAGE_URL = f"{MEDIA_URL}" + "{image}"
BONUS_URL = f"{MEDIA_URL}bonus/" + "{image}"


bp = Blueprint('nicht_lustig_archive', __name__, url_prefix='/nl')
cache = Cache()

@bp.get("/all")
@cache.cached(timeout=3600)
def get_cartoons_list():
    soup = BeautifulSoup(requests.get(BASE_URL).content, "html.parser")
    # As the list is embedded inside of a javascript tag we cannot utilise bs4 any further but to find all occurances of script-tags.
    reg = re.compile(r"var cartoonList = (\[.*?\]);")

    # Also we have to make the cartoonlist json-readable ie replace single-quotes with double-qoutes
    scripts = [
        sear.group(1) for sear in [reg.search(scr.text.replace("'", '"')) for scr in soup.findAll("script")] if sear
    ]
    cartoons_list = []
    for script in scripts:
        # Remove anything decorativ/we like tabs, excessive spaces.
        script = script.replace('\t', "").replace(' "', '"').replace('" ', '"')
        # Remove trailing colons
        script = script.replace(",]", "]")
        cartoons_list.extend(json.loads(script))

    # Ensure no duplicates
    cartoons_list = [a[0] for a in itertools.groupby(cartoons_list)]
    return cartoons_list


def get_bonus_cartoons_list() -> List:
    return list(filter(lambda cartoon: cartoon['public_bonus'], get_cartoons_list()))


def get_uri(*cartoons) -> List:
    uri_list = []
    for cartoon in cartoons:
        uri_list.append(IMAGE_URL.format(image=cartoon["image"]))
        if cartoon["public_bonus"]:
            uri_list.append(BONUS_URL.format(image=cartoon["bonus_image"]))
    return uri_list


def get_random_cartoon(count: int = 1):
    return get_uri(*random.sample(get_cartoons_list(), count))


def get_random_bonus_cartoon(count: int = 1):
    return get_uri(*random.sample(get_bonus_cartoons_list(), count))


def get_cartoons_list_by_tag(tag: str) -> List:
    return list(filter(lambda cartoon: tag in cartoon['tags'], get_cartoons_list()))


def get_bonus_cartoons_list_by_tag(tag: str) -> List:
    return list(filter(lambda cartoon: tag in cartoon['tags'], get_bonus_cartoons_list()))


def main():
    print(get_random_cartoon())


if __name__ == '__main__':
    main()
