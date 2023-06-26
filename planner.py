from print_utils import Printer
from node import Node, compute_drive_statistics, compute_distancetoreach, compute_heuristic
from utils import distance_on_earth, distance_on_earth_nodes
from global_vars import velocity, max_dist, verbose
from utils import plot_superchargers_with_path
import pandas as pd


def planner(start_node,goal_node,nodes):
	openset = dict()
	closedset = dict()

	compute_heuristic(start_node,goal_node)
	# print(start_node.get_details())

	openset[start_node.id] = start_node

	while len(openset)>0:
		current_id = min(openset, key=lambda o: openset[o].heuristic)
		current = openset[current_id]

		Printer.yellow(current.get_details())

		if(current.id == goal_node.id):
			Printer.green("Goal reached!")
			return current

		del openset[current_id]
		closedset[current_id] = current

		for i in range(len(nodes)):
			distance_from_current = distance_on_earth_nodes(current,nodes[i])
			if distance_from_current <= max_dist:

				compute_drive_statistics(current,nodes[i])
				compute_heuristic(nodes[i],goal_node)

				# Printer.green(current)
				# Printer.purple(distance_on_earth_nodes(current,nodes[i]))
				# Printer.red(nodes[i].get_details())

				if nodes[i].id in closedset:
						if verbose: Printer.cyan(nodes[i])
						continue

				if nodes[i].id not in openset:
						if verbose: Printer.green(nodes[i])
						nodes[i].set_parent(current)
						openset[nodes[i].id] = nodes[i]  # Discover a new node

				else:
						if openset[nodes[i].id].heuristic >= nodes[i].get_heuristic():
							if verbose: Printer.yellow(nodes[i])
							openset[nodes[i].id] = nodes[i]

	Printer.red("Goal not found!")
	return None


def backtrack(current):
	path = []
	while current:
		# print(current)
		current.compute_distance_from_parent()
		path.append([current.id,current.lat,current.lng,current.charging_rate,current.distancefromparent,current.heuristic,current.remaining_fuel_distance,current.get_charge_time()])
		current = current.parent

	path = path[::-1]
	return path

def display_path(data,path,plot=True):
	if path is not None:
		pathdf = pd.DataFrame(path, columns = ['Location', 'lat','lng','charging_rate','dist_from_parent','heuristic','remaining_fuel_distance','time_spent_charging'])
		# pathdf.loc[:,'time_spent_charging'] = [x.get_charge_time() for x in path] #pathdf['dist_from_parent']/pathdf['charging_rate']
		pathdf['time_spent_driving'] = pathdf['dist_from_parent']/velocity
		pathdf['time_spent'] =  pathdf['time_spent_charging'] + pathdf['time_spent_driving']
		pathdf = pathdf.replace(float('inf'), 0)
		pathdf['total_time_spent'] = pathdf['time_spent'].cumsum()
		plot_superchargers_with_path(data,pathdf)
		print_path_results(pathdf)

def print_path_results(pathdf):
	Printer.yellow("Path Results:")
	print(pathdf)



