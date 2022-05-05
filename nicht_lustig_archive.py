import itertools
import json
import random
import re

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://joscha.com/nichtlustig"
MEDIA_URL = "https://joscha.com/data/media/cartoons/"
IMAGE_URL = f"{MEDIA_URL}"+"{image}"
BONUS_URL = f"{MEDIA_URL}bonus/"+"{image}"

def get_cartoons_list():
	"""Fetch the landing page of nichtlustig and scrape js for a list of all available cartoon panels.

	- **return** and **return types**::

		:return: returns a json-compatible list of cartoonpanels
		:rtype: list containing dictionaries describing each panel

	"""
	soup = BeautifulSoup(requests.get(BASE_URL).content, "html.parser")
	reg = re.compile("var cartoonList = (\[.*?\]);")
	scripts = [reg.search(scr.text.replace("'",'"')).group(1) for scr in soup.findAll("script") if reg.search(scr.text)]
	cartoons_list = []
	for script in scripts:
		script = script.replace('\t',"").replace(' "', '"').replace('" ', '"')
		script = script.replace(",]", "]")
		cartoons_list.extend(json.loads(script))
	cartoons_list = [a[0] for a in itertools.groupby(cartoons_list)]
	return cartoons_list

def get_uri(*cartoons)->list():
	"""Produce a list of URIs pointing to every publicly accessible panel for a given cartoon-dictionary as produced by get_cartoon_list().

	- **parameters**, **types**, **return** and **return types**::

		:param cartoons: Any amount of dictionaries describing cartoon-panels
		:type cartoons: dictionaries
		:return: returns a list of cartoon panels (Including publicly accessible bonus panels)
		:rtype: list containing dictionaries describing each panel

	"""
	uri_list = []
	for cartoon in cartoons:
		uri_list.append(IMAGE_URL.format(image=cartoon["image"]))
		if cartoon["public_bonus"]:
			uri_list.append(BONUS_URL.format(image=cartoon["bonus_image"]))
	return uri_list

def get_random_cartoon(count:int = 1):
	"""Produce a random selection of N cartoon URIs.

	- **parameters**, **types**, **return** and **return types**::

		:param count: How many cartoons do you want?
		:type count: int
		:return: List of cartoon panels
		:rtype: list containing str

	"""
	return get_uri(*random.sample(get_cartoons_list(), count))

def get_random_bonus_cartoon(count:int = 1):
	"""Produce a random selection of N cartoon URIs with bonus panels (in sum 2*count URIs).

	- **parameters**, **types**, **return** and **return types**::

		:param count: How many cartoons do you want?
		:type count: int
		:return: List of cartoon panels
		:rtype: list containing str

	"""
	return get_uri(*random.sample(list(filter(lambda cartoon: cartoon['public_bonus'], get_cartoons_list())), count))

def main():
	print(get_random_cartoon())

if __name__ == '__main__':
	main()
