import numpy as np
import pandas as pd

def shortest_path(s, nodes, edges, length_mat):

	'''
	Compute shortest path tree from source node
	INPUT
	s - source node 
	Nodes <np.array>
	Edges <np.array>
	+----+----+------+
	 Tail|Head|Weight
	+----+----+------+
	OUTPUT
	Predecessors <np.array>
	Shortest path lengths <np.array>

	Details:
	O(mn) label correcting implementation
	Does not handle negative cycles (easy to implement)
	'''

	# Check if negative values are in list
	if np.amin(length_mat) < 0:
		raise Exception('Graph May Contain Negative Cycle')

	# Set up label and predecessor lists
	label = np.array([0 if i == s else np.Inf for i in nodes])
	pred_list = np.array([np.Inf for i in nodes])

	# Initialize queue
	process = [s]

	# Correct shortest path labels
	while process:
		node = process.pop(0)
		for edge in edges[edges[:,0] == node]:		
			head = edge[1]
			if label[head] > label[node] + length_mat[node, head]:
				label[head] = label[node] + length_mat[node, head]
				pred_list[head] = node
				if head not in process:
					process.append(head)

	return((label, pred_list))
		

# TEST CASE 
# s = 0
# nodes = np.arange(4)
# edges = np.array([[0, 1, 5],
# 	[0, 2, 2],
# 	[1, 3, 1],
# 	[2, 1, 1],
# 	[2, 3, 5]])


def shortest_path_tau(s, T, nodes, edges, length_mat):
	'''
	Compute from source node
	INPUT
	s - source node 
	T - upper bound on tau <int>
	nodes <np.array>
	edges <np.array>
	+----+----+---+
	 Tail|Head|tau
	+----+----+---+
	
	length_mat <np.array>
		contains length of each edge if it exists

	OUTPUT
	Predecessors <np.array>
		entry (i, t) is -1 if no path from s -> i with cumulative tau < t 
	Shortest path lengths <np.array>

	Details:
	Does not handle negative cycles (easy to implement)
	'''

	# Initialize label and precendence
	label = np.empty((len(nodes), T+1))
	label[:,:] = np.Inf
	label[:,0] = np.array([0 if node == s else np.Inf for node in nodes])

	precedence = np.empty((len(nodes), T+1))
	precedence[:,:] = -1
	precedence[s,0] = s
	
	# Updating loop (dynamic programming)
	for t in range(1, T+1): # iteration for each tau value
		for node in nodes: # update each node
			vals = [[label[node, t-1], precedence[node, t-1]]] # list of candidate arcs
			for edge in edges[edges[:,1] == node]: # edges with current node as head
				if edge[2] <= t: # verify tau not exceeded
					tail = edge[0].astype(int)
					head = edge[1].astype(int)
					tau_index = np.floor(t - edge[2]).astype(int)
					vals.append([label[tail, tau_index] + length_mat[tail, head], tail])
			# choose best arc and update accordingly
			vals = np.array(vals)
			ind = np.where(vals[:,0] == np.amin(vals[:,0]))[0][0]
			label[node, t:] = vals[ind, 0]
			precedence[node, t:] = np.floor(vals[ind, 1]).astype(int)
			#pred_list[node] = vals[np.where(vals == np.amin(vals))][0]
	precedence = precedence.astype('int')
	return (label, precedence)

def generate_tau_paths(s, edges, precedence):
	'''
	INPUT
	s <int> source node

	edges <np.array>
	+-----+-----+---+
	 Tail |Head | t |
	+-----+-----+---+

	precedence <np.array>
	     Tau value
		+--------------+	
	node|preceding node|
		+--------------+
	
	OUTPUT
	paths <list(list(int))>
	all path found in the tau algorithm
	'''

	nodes, Tau = precedence.shape # compute number of nodes and Tau
	paths = [] # initialize paths
	for node in range(nodes): # generate path for each node

		if precedence[node, Tau-1] != -1: # check if path exists
			
			rem_tau = Tau-1
			path = []
			curr_node = node
			path.append(curr_node)

			while curr_node != s: # continue until source node reached
				next_node = precedence[curr_node, rem_tau]

				# Grab the preceding node
				# little complicated to handle multiedges
				edge_inds = np.where((edges[:,0]==next_node) & (edges[:,1] == curr_node))[0]
				edge_inds_tau = np.array([[ind, edges[ind, 2]] for ind in edge_inds])
				ind = np.argsort(edge_inds_tau[:,1])[0]
				edge_ind = int(edge_inds_tau[ind,0])

				# Update tau and current node
				rem_tau -= edges[edge_ind, 2]
				rem_tau = np.floor(rem_tau).astype('int')
				curr_node = int(next_node)
				path.append(curr_node)

			paths.append(path) # add path to list

	return paths




































