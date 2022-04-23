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
		

# TEST CASE 1
# s = 0
# nodes = np.arange(4)
# edges = np.array([[0, 1, 5],
# 	[0, 2, 2],
# 	[1, 3, 1],
# 	[2, 1, 1],
# 	[2, 3, 5]])

# path = shortest_path(s, nodes, edges)
# print(path)

# TEST

# edge_data = np.genfromtxt("edge_data.csv", delimiter=",")
# edge_clean = edge_data[1:,1:-1].astype(int)
# edge_clean[:,0:2] = edge_clean[:,0:2]-1

# rev_arcs = edge_clean[:,[1, 0, 2]]
# edge_clean = np.concatenate((edge_clean, rev_arcs), axis = 0)

# nodes = np.arange(0,1114)



# paths = shortest_path(176, nodes, edge_clean)
# print(sorted(paths[0])[0:50])

def shortest_path_tau(s, T, nodes, edges, length_mat):
	'''
	Compute from source node
	INPUT
	s - source node 
	T - upper bound <int>
	Nodes <np.array>
	Edges <np.array>
	+----+----+--------+-+
	 Tail|Head|Distance|t
	+----+----+--------+-+
	OUTPUT
	Predecessors <np.array>
	Shortest path lengths <np.array>

	Details:
	Does not handle negative cycles (easy to implement)
	'''

	# Initialize labels
	label = np.empty((len(nodes), T+1))
	precedence = np.empty((len(nodes), T+1))
	precedence[:,:] = -1
	precedence[s,0] = s
	label[:,:] = np.Inf
	label[:,0] = np.array([0 if node == s else np.Inf for node in nodes])

	# Initialize pred list
	#pred_list = np.array([np.Inf for i in nodes])

	# Updating loop
	for t in range(1, T+1):
		for node in nodes:
			vals = [[label[node, t-1],0]]
			for edge in edges[edges[:,1] == node]:
				if edge[2] <= t:
					tail = edge[0].astype(int)
					head = edge[1].astype(int)
					tau_index = np.floor(t - edge[2]).astype(int)
					vals.append([label[tail, tau_index] + length_mat[tail, head], tail])
			vals = np.array(vals)
			ind = np.where(vals[:,0] == np.amin(vals[:,0]))[0][0]
			label[node, t:] = vals[ind, 0]
			precedence[node, t:] = np.floor(vals[ind, 1]).astype(int)
			#pred_list[node] = vals[np.where(vals == np.amin(vals))][0]
	precedence = precedence.astype('int')
	print(precedence.dtype)
	return (label, precedence)
	#return (label, pred_list)
	# Add in predecessor handler

# TEST CASE 1
# s = 0
# T = 4
# nodes = np.arange(4)
# edges = np.array([[0, 1, 5, 2],
# 	[0, 2, 2, 1],
# 	[1, 3, 1, 2],
# 	[2, 1, 1, 7],
# 	[2, 3, 5, 1]])

# shortest_path_tao(s, T, nodes, edges)

# load and convert to numpy array
link = "https://raw.githubusercontent.com/DillWithIt77/D2P_Spring_2022/main/edge_data_updated.csv"
data = pd.read_csv("https://raw.githubusercontent.com/DillWithIt77/D2P_Spring_2022/main/edge_data_updated.csv")
data = data.to_numpy()

# chop off row indices
data = data[:,1:]

#sort data by rows
data = data[data[:, 0].argsort()]

#add reversed edges
data_rev = data[:, [1, 0, 2, 3]]
data = np.vstack((data, data_rev))
road_type = data[:,3]

#max edge is 1059
nodes = np.arange(0,1060)

edges = data[:,:2]
lengths = data[:,2]
# convert lengths to miles 1,609.344
lengths = lengths/1609.344

# make edges integers
edges = edges.astype(int)


# define lengths matrix
length_mat = np.zeros((1060, 1060))
for i in range(len(edges)):
	length_mat[edges[i, 0], edges[i, 1]] = lengths[i]



# dat_l, dat_pl = shortest_path(26, nodes, edges, length_mat)
# print(sorted(dat_l)[-2])

'''
auraria_label, auraria_predlist = shortest_path(26, nodes, edges, length_mat)
auraria_res = list(zip(auraria_label, auraria_predlist))
auraria_res_df = pd.DataFrame(auraria_res)
auraria_res_df.to_csv('auraria_res.csv')

union_label, union_predlist = shortest_path(433, nodes, edges, length_mat)
union_res = list(zip(union_label, union_predlist))
union_res_df = pd.DataFrame(union_res)
union_res_df.to_csv('union_res.csv')

citypark_label, citypark_predlist = shortest_path(834, nodes, edges, length_mat)
citypark_res = list(zip(citypark_label, citypark_predlist))
citypark_res_df = pd.DataFrame(citypark_res)
citypark_res_df.to_csv('citypark_res.csv')

DU_label, DU_predlist = shortest_path(427, nodes, edges, length_mat)
DU_res = list(zip(DU_label, DU_predlist))
DU_res_df = pd.DataFrame(DU_res)
DU_res_df.to_csv('DU_res.csv')

DCM_label, DCM_predlist = shortest_path(112, nodes, edges, length_mat)
DCM_res = list(zip(DCM_label, DCM_predlist))
DCM_res_df = pd.DataFrame(DCM_res)
DCM_res_df.to_csv('DCM_res.csv')
'''



'''
Tau values for roads 
Values from UBC Paper of Route Preferences

Name - Number - Tau
Bike Lane - 0 - 4 - Everywhere
Buffered Bike Lane (no barrier) - 1 - 2 - Champa from MLK to 19th
Neighborhood Bikeway - 2 - 1 - 35th Ave
Protected Bike Lane (barrier) - 3 - 2 - Marion St Pkwy
Shared Roadway - 4 - 6 - Everywhere
Shared Use Path - 5 - 0 - CCT
Trail - 6 - 0 - South Platt River


Pref:
MUP (6, 5) > NBW (2) > PBL (1,3) >> BL (0) >> SL (4) 
'''

tau_dict = {
	0:4,
	1:2,
	2:1,
	3:2,
	4:6,
	5:0,
	6:0
}

tau_col = np.array([lengths[i]*tau_dict[road_type[i]] for i in range(len(lengths))])
tau_col = np.reshape(tau_col, (1, 2490))

edges = np.hstack((edges, tau_col.transpose()))

label, precedence = shortest_path_tau(26, 11, nodes, edges, length_mat)

final_labels = label[:,-1]
test = np.sort(final_labels)

# Cautious Biker
# tau = 10
# Equivalent to 5 miles on Protected Bike Lane
# 10 miles on Neighborhood Bikeway
# 2.5 miles on a protected bike lane
# Unlimited miles on a shared path

# Auraria Cautious

label, precedence = shortest_path_tau(26, 11, nodes, edges, length_mat)
np.savetxt("auraria_tau_distances_cautious.csv", label, delimiter=",")
np.savetxt("auraria_tau_precedence_cautious.csv", precedence, fmt='%i', delimiter=",")

print("a cautious finished")

# Union Cautious

label, precedence = shortest_path_tau(433, 11, nodes, edges, length_mat)
np.savetxt("union_tau_distances_cautious.csv", label, delimiter=",")
np.savetxt("union_tau_precedence_cautious.csv", precedence, fmt='%i', delimiter=",")

print("U cautious finished")

# City Park Cautious

label, precedence = shortest_path_tau(834, 11, nodes, edges, length_mat)
np.savetxt("citypark_tau_distances_cautious.csv", label, delimiter=",")
np.savetxt("citypark_tau_precedence_cautious.csv", precedence, fmt='%i', delimiter=",")

print("CP cautious finished")

# DU Cautious

label, precedence = shortest_path_tau(427, 11, nodes, edges, length_mat)
np.savetxt("DU_tau_distances_cautious.csv", label, delimiter=",")
np.savetxt("DU_tau_precedence_cautious.csv", precedence, fmt='%i', delimiter=",")

print("DU cautious finished")

# Five Points/DCM Cautious

label, precedence = shortest_path_tau(112, 11, nodes, edges, length_mat)
np.savetxt("5points_tau_distances_cautious.csv", label, delimiter=",")
np.savetxt("5points_tau_precedence_cautious.csv", precedence, fmt='%i', delimiter=",")

print("5P cautious finished")

# Riskier Biker
# tau = 20
# Equivalent to 10 miles on Protected Bike Lane
# 20 miles on Neighborhood Bikeway
# 5 miles on a protected bike lane
# Unlimited miles on a shared path

# Auraria Cautious

label, precedence = shortest_path_tau(26, 21, nodes, edges, length_mat)
np.savetxt("auraria_tau_distances_risky.csv", label, delimiter=",")
np.savetxt("auraria_tau_precedence_risky.csv", precedence, fmt='%i', delimiter=",")

print("a risky finished")

# Union Cautious

label, precedence = shortest_path_tau(433, 21, nodes, edges, length_mat)
np.savetxt("union_tau_distances_risky.csv", label, delimiter=",")
np.savetxt("union_tau_precedence_risky.csv", precedence, fmt='%i', delimiter=",")

print("U risky finished")

# City Park Cautious

label, precedence = shortest_path_tau(834, 21, nodes, edges, length_mat)
np.savetxt("citypark_tau_distances_risky.csv", label, delimiter=",")
np.savetxt("citypark_tau_precedence_risky.csv", precedence, fmt='%i', delimiter=",")

print("CP risky finished")

# DU Cautious

label, precedence = shortest_path_tau(427, 21, nodes, edges, length_mat)
np.savetxt("DU_tau_distances_risky.csv", label, delimiter=",")
np.savetxt("DU_tau_precedence_risky.csv", precedence, fmt='%i', delimiter=",")

print("DU risky finished")

# Five Points/DCM Cautious

label, precedence = shortest_path_tau(112, 21, nodes, edges, length_mat)
np.savetxt("5points_tau_distances_risky.csv", label, delimiter=",")
np.savetxt("5points_tau_precedence_risky.csv", precedence, fmt='%i', delimiter=",")

print("Finished")

























