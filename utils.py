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

	tmp = pathdf.select_dtypes(include=[np.float64])
	pathdf.loc[:, tmp.columns] = np.round(tmp,2)

	pathdf['val'] = "Distance to reach "+pathdf.Location.astype(str)+": "+pathdf.dist_from_parent.astype(str)+"<br>Charging Rate of station:"+pathdf.charging_rate.astype(str)+"<br>Charging Time:"+pathdf.time_spent_charging.astype(str)+"<br>Driving Time:"+pathdf.time_spent_driving.astype(str)+"<br>Total Time spent to reach station and charge:"+pathdf.time_spent.astype(str)+"<br>Total Time spent cumulative:"+pathdf.total_time_spent.astype(str)



	charge_cond = pathdf.time_spent_charging > 0
	charge_df = pathdf[charge_cond]

	cond = data['Location'].isin(pathdf['Location'])
	data.drop(data[cond].index, inplace = True)
	print(pathdf.columns)

	plots = [
     	# go.Scattergeo(
        # hoverinfo='none',
		# lon = data.lng,
		# lat = data.lat,
		# # text = data.val,
		# mode = 'markers',
		# marker = dict(
		# 	size = 8,
		# 	opacity = 0.5,
		# 	reversescale = False,
		# 	autocolorscale = False,
		# 	cmin = data.charging_rate.min(),
		# 	color = data.charging_rate,
		# 	cmax = data.charging_rate.max(),
		# 	colorbar_title="Charging Rate")
		# ),
		# go.Scattergeo(
		# lon = pathdf.lng,
		# lat = pathdf.lat,
		# text = pathdf.val,
		# mode = "lines",
		# line = dict(width=4, dash='dash'),

		# marker = dict(
		# 	size = 8,
		# 	opacity = 1,
		# 	reversescale = False,
		# 	autocolorscale = False,
		# 	cmin = data.charging_rate.min(),
		# 	color = data.charging_rate,
		# 	cmax = data.charging_rate.max(),
		# 	colorbar_title="Charging Rate")
  		# ),

		# go.Scattermapbox(
		# mode = "markers",
		# lon = pathdf.lng,
		# lat = pathdf.lat,
		# marker = { 'symbol': "fuel", 'opacity':1, 'allowoverlap': True,"size" :5,},
		# hoverinfo='skip'),

		go.Scattermapbox(
		# hoverinfo='none',
		# text = pathdf.val,
		lon = data.lng,
		lat = data.lat,
        mode='markers',
        marker = {'size': 5,
                  'symbol': ["fuel"]*len(data),
                  'allowoverlap': True,
                #   'color': pathdf.charging_rate,
                  'cmin': data.charging_rate.min(),
                  'cmax': data.charging_rate.max()
                }),

		go.Scattermapbox(
		text = pathdf.val,
		lon = pathdf.lng,
		lat = pathdf.lat,
        mode='markers+lines',
        marker = {'size': 8,
                  'symbol': ["fuel"]*len(pathdf),
                  'allowoverlap': True,
                #   'color': pathdf.charging_rate,
                }
    	),


			]

	fig = go.Figure(data=plots)

	fig.update_layout(
			title = 'Tesla Supercharger Network',
			geo_scope='usa',
			showlegend=False,
			mapbox = dict(
			accesstoken="pk.eyJ1IjoidmlzaGFsZ2F0dGFuaTEwIiwiYSI6ImNqazdvZjU1ajIwc24za241Ynp0b3FiMjIifQ.KOjDXUbj17uYUWgo_aFKQA",
			bearing=0,
			center=dict(
				lat=38.92,
				lon=-99.3
			),
			pitch=0,
			zoom=3.5
    ),
		)

	fig.update_traces(name='Station', showlegend = False)



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

	# phi1 = (90.0 - lat1) * degrees_to_radians
	# phi2 = (90.0 - lat2) * degrees_to_radians


	# theta = longitude
	theta1 = long1 * degrees_to_radians
	theta2 = long2 * degrees_to_radians

	# Compute spherical distance from spherical coordinates.
	cos = (np.sin(phi1) * np.sin(phi2)* np.cos(theta1 - theta2) +
		   np.cos(phi1) * np.cos(phi2))
	arc = np.arccos(cos)
	rv = arc * radius

	return rv
