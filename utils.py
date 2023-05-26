import pandas as pd
import math
import random
import warnings
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from global_vars import min_charging_rate, max_charging_rate ,decimal_places ,verbose ,velocity ,max_dist ,earth_radius, parse

def read_csv(filename):
	df = pd.read_csv(filename)
	return df

def add_random_charging_rates(data,min_range=80,max_range=180):
	if 'charging_rate' in data.columns:
		warnings.warn("'charging_rate' exists in columns. Dropping column.")
		data = data.drop('charging_rate', axis=1)

	charging_rates = []
	for i in range(0, len(data)):
		rate = random.uniform(min_range, max_range)
		charging_rates.append(rate)

	data['charging_rate'] = charging_rates
	data.charging_rate = data.charging_rate.round(3)
	return data


def distance_on_earth(lat1, long1, lat2, long2, radius=earth_radius):
	"""
	Compute distance between two points on earth specified by latitude/longitude.
	The earth is assumed to be a perfect sphere of given radius. The radius defaults
	to 6378.388 kilometers. To convert to miles, divide by 1.60934

	Reference
	---------
	Adopted from John D. Cook's blog post:
	http://www.johndcook.com/blog/python_longitude_latitude/
	"""
	# radius = 6378.388
	# Convert latitude and longitude to spherical coordinates in radians.
	degrees_to_radians = np.pi / 180.0

	# phi = 90 - latitude
	phi1 = (90.0 - lat1) * degrees_to_radians
	phi2 = (90.0 - lat2) * degrees_to_radians

	# theta = longitude
	theta1 = long1 * degrees_to_radians
	theta2 = long2 * degrees_to_radians

	# Compute spherical distance from spherical coordinates.
	cos = (np.sin(phi1) * np.sin(phi2)* np.cos(theta1 - theta2) +
		   np.cos(phi1) * np.cos(phi2))
	arc = np.arccos(cos)
	rv = arc * radius
	return rv




def plot_superchargers(data):
	data['val'] = data.Location.astype(str)+": "+data.charging_rate.astype(str)
	fig = go.Figure(data=go.Scattergeo(
		lon = data.lng,
		lat = data.lat,
		text = data.val,
		mode = 'markers',
		marker = dict(
			size = 8,
			opacity = 0.8,
			reversescale = False,
			autocolorscale = False,
			cmin = data.charging_rate.min(),
			color = data.charging_rate,
			cmax = data.charging_rate.max(),
			colorbar_title="Charging Rate"
		)))


	fig.update_layout(
			title = 'Tesla Supercharger Network',
			geo_scope='usa',

		)
	fig.show()

def plot_superchargers_with_path(data,pathdf):
	data['val'] = data.Location.astype(str)+": "+data.charging_rate.astype(str)
	pathdf['val'] = pathdf.Location.astype(str)+": "+pathdf.dist_from_parent.astype(str)

	plots = [go.Scattergeo(
		lon = data.lng,
		lat = data.lat,
		text = data.val,
		mode = 'markers',
		marker = dict(
			size = 8,
			opacity = 0.8,
			reversescale = False,
			autocolorscale = False,
			cmin = data.charging_rate.min(),
			color = data.charging_rate,
			cmax = data.charging_rate.max(),
			colorbar_title="Charging Rate"
		)),
			go.Scattergeo(
		lon = pathdf.lng,
		lat = pathdf.lat,
		text = pathdf.val,
		mode = 'markers+lines',
		marker = dict(
			size = 1,
			opacity = 0.01,
			reversescale = False,
			autocolorscale = False,
			cmin = data.charging_rate.min(),
			color = data.charging_rate,
			cmax = data.charging_rate.max(),
			colorbar_title="Charging Rate"

		))

			]

	fig = go.Figure(data=plots)

	fig.update_layout(
			title = 'Tesla Supercharger Network',
			geo_scope='usa',
			showlegend=False

		)
	fig.show()




def distance_on_earth_nodes(node1, node2, radius=6356.752):
	"""
	Compute distance between two points on earth specified by latitude/longitude.
	The earth is assumed to be a perfect sphere of given radius. The radius defaults
	to 6378.388 kilometers. To convert to miles, divide by 1.60934
	"""
	# radius = 6356.752
	# Convert latitude and longitude to spherical coordinates in radians.
	degrees_to_radians = np.pi / 180.0
	lat1 = node1.lat
	long1 = node1.lng
	lat2 = node2.lat
	long2 = node2.lng

	dlat = math.radians(lat2 - lat1)
	dlon = math.radians(long2 - long1)
	a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2))
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	d = radius * c

	# phi = 90 - latitude
	phi1 = (lat1) * degrees_to_radians
	phi2 = (lat2) * degrees_to_radians

	# theta = longitude
	theta1 = long1 * degrees_to_radians
	theta2 = long2 * degrees_to_radians

	# Compute spherical distance from spherical coordinates.
	cos = (np.sin(phi1) * np.sin(phi2)* np.cos(theta1 - theta2) +
		   np.cos(phi1) * np.cos(phi2))
	arc = np.arccos(cos)
	rv = arc * radius

	return rv
