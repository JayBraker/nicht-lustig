import itertools
import json
import random
import re

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://joscha.com/nichtlustig"
IMAGE_URL = "https://joscha.com/data/media/cartoons/{image}"

def get_cartoons_list():
    soup = BeautifulSoup(requests.get(BASE_URL).content)
    reg = re.compile("var cartoonList = (\[.*?\]);")
    scripts = [reg.search(scr.text.replace("'",'"')).group(1) for scr in soup.findAll("script") if reg.search(scr.text)]
    cartoons_list = []
    for script in scripts:
        script = script.replace('\t',"").replace(' "', '"').replace('" ', '"')
        script = script.replace(",]", "]")
        cartoons_list.extend(json.loads(script))
    cartoons_list = [a[0] for a in itertools.groupby(cartoons_list)]
    return cartoons_list

def main():
    #print(get_cartoons_list())
    print(IMAGE_URL.format(image=random.choice(get_cartoons_list())["image"]))

if __name__ == '__main__':
    main()
