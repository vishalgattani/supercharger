import numpy as np
import pandas as pd
import sys
import os
import warnings
import chart_studio
import chart_studio.plotly as cspy
import chart_studio.tools as tls
from queue import PriorityQueue


from sample_data import network
from tesla_supercharger_web_parser import tesla_supercharger_parser
from print_utils import Printer
from utils import read_csv, add_random_charging_rates, plot_superchargers, plot_superchargers_with_path
from planner import planner, backtrack, print_path_results, display_path
from node import Node
from credentials import username, api_key
from global_vars import min_charging_rate, max_charging_rate ,decimal_places ,verbose ,velocity ,max_dist ,earth_radius, parse, webscraper_data, data_directory

if not os.path.exists(data_directory):
	    # If it doesn't exist, create it
	    os.makedirs(data_directory)

chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
os.system('cls' if os.name == 'nt' else 'clear')


if parse:
	tesla_supercharger_parser()

if webscraper_data:
	data = read_csv(data_directory+"supercharger-1.csv")
	data.columns = ["Location","lat","lng"]
	data = add_random_charging_rates(data,min_charging_rate,max_charging_rate)
	df = data.sample(n=2)
	start_idx = df.index.tolist()[0]
	goal_idx = df.index.tolist()[1]
	start = data.iloc[start_idx]
	goal = data.iloc[goal_idx]

	start_node = Node(start.Location,start.lat,start.lng,start.charging_rate)
	goal_node = Node(goal.Location,goal.lat,goal.lng,goal.charging_rate)

else:
	network_df = pd.DataFrame(network,columns=["Location","lat","lng","charging_rate"])
	network_df.to_csv(data_directory+"network.csv")
	data = network_df
	start = data[data.Location=="Council_Bluffs_IA"]
	goal = data[data.Location=="Cadillac_MI"]
	start_idx = start.index[0]
	goal_idx = goal.index[0]
	start_node = Node(start.Location.values.tolist()[0],start.lat.values.tolist()[0],start.lng.values.tolist()[0],start.charging_rate.values.tolist()[0])
	goal_node = Node(goal.Location.values.tolist()[0],goal.lat.values.tolist()[0],goal.lng.values.tolist()[0],goal.charging_rate.values.tolist()[0])

query = data.copy()
query = query.drop([start_idx])

nodes = []
for i in range(len(query)):
	row = query.iloc[i]
	sample = Node(row.Location,row.lat,row.lng,row.charging_rate)
	nodes.append(sample)

# my planner

start_node.set_remaining_fuel_distance(max_dist)

status = planner(start_node,goal_node,nodes)
if isinstance(status, Node):
	path = backtrack(status)
	display_path(data,path)
else:
	path = None
	warnings.warn("Planner couldn't find a path. Terminating...")
	sys.exit()


# new planner



