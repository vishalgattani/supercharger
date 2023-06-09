import math
from utils import distance_on_earth, distance_on_earth_nodes
from global_vars import velocity ,max_dist, earth_radius

def compute_drive_statistics(node1,node2):
	if node1.id != node2.id:
		dist = compute_distancetoreach(node1,node2)
		# assuming it has to full charge any way at the destination charging station
		# if dist <= max_dist:
		# 	node2.set_drivetimetoreach(dist/velocity)
		# 	node2.set_distancetoreach(dist)
		# 	timetocharge = dist/node2.get_charging_rate()
		# 	node2.set_charge_time(timetocharge)
		# else:
		# 	node2.set_drivetimetoreach(float('inf'))
		# 	node2.set_distancetoreach(float('inf'))
		# 	timetocharge = float('inf')
		# 	node2.set_charge_time(timetocharge)

		if dist <= node1.remaining_fuel_distance:
			if node1.charging_rate >= node2.charging_rate:
				# charge at node 1 enough (full?) to reach node 2 so charging time at node 1 = 320.0 - node1.remaining_fuel_distance / charging rate at node 1
				node2.set_drivetimetoreach(dist/velocity)
				node2.set_distancetoreach(dist)
				timetocharge = dist/node1.get_charging_rate()
				node2.set_remaining_fuel_distance(node1.remaining_fuel_distance-dist)
				node1.set_charge_time(timetocharge)
			else:
				# charge at node 2 so charging time at node 1 = 0
				node2.set_drivetimetoreach(dist/velocity)
				node2.set_distancetoreach(dist)
				timetocharge = 0.0
				node2.set_remaining_fuel_distance(node1.remaining_fuel_distance-dist)
				node1.set_charge_time(timetocharge)
		else:
			# charge at node 1 enough to reach node 2 so charging time at node 1 = distance to node 2 / charging rate at node 1
			node2.set_drivetimetoreach(dist/velocity)
			node2.set_distancetoreach(dist)
			timetocharge = dist/node1.get_charging_rate()
			node2.set_remaining_fuel_distance(node1.remaining_fuel_distance-dist)
			node1.set_charge_time(timetocharge)



def compute_distancetoreach(node1,node2,max_dist=max_dist):
	return distance_on_earth_nodes(node1,node2)

def compute_heuristic(node,goal,velocity=velocity,max_dist=max_dist):
	"""_summary_
		time spent in totality = drive time to reach a node + charging time + distance to goal / velocity
	"""
	distance_from_goal = compute_distancetoreach(node,goal)
	node.set_distancefromgoal(distance_from_goal)
	if distance_from_goal !=0:
		heuristic = node.get_drivetimetoreach() + node.get_charge_time() + node.get_distancefromgoal()/velocity + 0.1*node.get_distancefromgoal()/node.get_charging_rate()
	else: heuristic = node.get_drivetimetoreach() + node.get_charge_time()
	heuristic = abs(heuristic)
	node.set_heuristic(heuristic)

class Node(object):
	def __init__(self,location,lat,lng,charging_rate) -> None:
		self.id = location
		self.lat = lat
		self.lng = lng
		self.charging_rate = charging_rate
		self.drivetimetoreach = 0
		self.chargingtime = 0
		self.distancetoreach = 0
		self.heuristic = 0.0
		self.parent = None
		self.distancefromgoal = None
		self.distancefromparent = float('inf')
		self.remaining_fuel_distance = 0.0

	# def __eq__(self, node: object) -> bool:
	#     return self.id == node.id

	def set_remaining_fuel_distance(self,remaining_fuel_distance):
		self.remaining_fuel_distance = remaining_fuel_distance

	def get_remaining_fuel_distance(self):
		return self.remaining_fuel_distance

	def get_details(self):
		if self.parent:
			self.distancefromparent = distance_on_earth_nodes(self,self.parent)
			return f"{self.id,(self.lat,self.lng),self.charging_rate,self.heuristic,self.distancefromgoal,self.parent.id,self.distancefromparent}"
		else:
			return f"{self.id,(self.lat,self.lng),self.charging_rate,self.heuristic,self.distancefromgoal}"

	def set_parent(self,parent):
		self.parent = parent
	def get_parent(self):
		return self.parent

	def compute_distance_from_parent(self):
		if self.parent:
			self.distancefromparent = distance_on_earth_nodes(self,self.parent)

	def set_charging_rate(self,charging_rate):
		self.charging_rate = charging_rate
	def get_charging_rate(self):
		return self.charging_rate

	def set_drivetimetoreach(self,drivetimetoreach):
		self.drivetimetoreach = drivetimetoreach
		if self.parent:
			self.drivetimetoreach += self.parent.drivetimetoreach
	def get_drivetimetoreach(self):
		return self.drivetimetoreach

	def set_distancetoreach(self, distancetoreach):
		self.distancetoreach = distancetoreach
	def get_distancetoreach(self):
		return self.distancetoreach

	def set_distancefromgoal(self, distancefromgoal):
		self.distancefromgoal = distancefromgoal
	def get_distancefromgoal(self):
		return self.distancefromgoal

	def set_charge_time(self,timetocharge):
		self.chargingtime = timetocharge
	def get_charge_time(self):
		return self.chargingtime

	def set_heuristic(self,heuristic):
		self.heuristic = heuristic
	def get_heuristic(self):
		return self.heuristic

	def __str__(self) -> str:
		return f"{self.id},{self.lat,self.lng,self.charging_rate}"
	 # return f"{self.id},{self.lat,self.lng,self.charging_rate},{self.drivetimetoreach:.2f},{self.distancetoreach:.2f},{self.chargingtime:.2f}"
	# return f"{self.id},{self.drivetimetoreach:.2f},{self.distancetoreach:.2f},{self.chargingtime:.2f},{self.heuristic:.2f}"
	# return f"{self.id},{self.heuristic:.2f}"

