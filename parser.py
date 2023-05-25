from bs4 import BeautifulSoup
import re
import requests
import numpy as np
import pandas as pd
from urllib.request import urlopen
from tqdm import tqdm
from global_vars import data_directory
import os

def tesla_supercharger_parser():

	Printer.yellow("Running webscraper...")
	# get the list of superchargers in the US
	url = 'http://www.teslamotors.com/findus/list/superchargers/United+States'
	rv = requests.get(url)
	content = rv.text
	# get link to each supercharger, each page contains the supercharger's coordinates
	sc_page_urls = re.findall('(/findus/location/supercharger/\w+)', content)
	# get the cooridnates (latitude, longitude) for each supercharger
	sc_names = []
	sc_coors = {}
	for sc_page_url in tqdm(sc_page_urls):
	    url = 'http://www.teslamotors.com' + sc_page_url
	    rv = requests.get(url)
	    soup = BeautifulSoup(rv.text)
	    sc_name = soup.find('h1').text
	    try:
	        directions_link = soup.find_all('a', href=True, string='Driving Directions')[0]
	        # print((directions_link))
	        lat, lng = directions_link['href'].split('=')[-1].split(',')
	        lat, lng = float(lat), float(lng)
	        # print(sc_name,lat,lng)
	        sc_names.append(sc_name)
	        sc_coors[sc_name] = {'lat': lat, 'lng': lng}
	    except:
	        ...
	# sort the names
	sc_names = sorted(sc_names)

	if not os.path.exists(data_directory):
	    # If it doesn't exist, create it
	    os.makedirs(data_directory)

	coords = pd.DataFrame.from_dict(sc_coors).T.reindex(sc_names)
	coords.to_csv(data_directory+"supercharger-1.csv")
	# coords.head()

	coords = pd.DataFrame.from_dict(sc_coors)
	coords.to_csv(data_directory+"supercharger-2.csv")
	# coords.head()

