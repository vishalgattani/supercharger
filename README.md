# supercharger
Finding the minimum time path through the tesla network of supercharging stations.

# 1. How to distribute the charging time at each station optimally?

- [x] Initial thought is to charge to full at every station to guarantee a valid path.
- [ ] This would be followed by reduction in the the overcharge value after a valid path is found.

# 2. How to find the shortest path with reasonable charging time?
- [x] Implement an A-Star like algorithm.
  - The cost function is an approximate one that combines information of distances and charging time which will favor the search toward a charging station that is closer to the goal.