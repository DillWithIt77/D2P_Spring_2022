from shortest_path import *
import numpy as np
import csv
import pandas as pd

# PREPROCESSING
# load and convert to numpy array
link = "https://raw.githubusercontent.com/DillWithIt77/D2P_Spring_2022/main/Data%20Cleaning%20and%20Plotting/edge_data_updated.csv"
data = pd.read_csv(link)
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
# convert lengths to miles from meters
lengths = lengths/1609.344

# make edges integers
edges = edges.astype(int)


# define lengths matrix
length_mat = np.zeros((1060, 1060))
for i in range(len(edges)):
	length_mat[edges[i, 0], edges[i, 1]] = lengths[i]

# COMPUTE SHORTEST PATHS
# 5 locations chosen, 26, 433, 834, 427, 112 are nodes representing 
# locations of Auraria, Union Station, City Park, University of Denver, and 
# Denver Central Market in 5 Points

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

# COMPUTE TAU PATHS CAUTIOUS AND RISKY 

'''
Tau values for roads 
Values derived from UBC Paper of Route Preferences

Name - Number - Tau
Bike Lane - 0 - 4 - Everywhere
Buffered Bike Lane (no barrier) - 1 - 2 - Champa from MLK to 19th
Neighborhood Bikeway - 2 - 1 - 35th Ave
Protected Bike Lane (barrier) - 3 - 2 - Marion St Pkwy
Shared Roadway - 4 - 6 - Everywhere
Shared Use Path - 5 - 0 - CCT
Trail - 6 - 0 - South Platt River


Pref:
Mixed Use Path (6, 5) > Neighborhood Bikeway (2) > Protected Bike Lane (1, 3)
 >> Bike Lane (0) >> Shared Lane (4) 
'''

# Create tau values and add to edges matrix
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

# COMPUTE TAU PATHS

# Auraria
s=26
edges=np.genfromtxt("edges_tau.csv", delimiter=",")

precedence=np.genfromtxt("auraria_tau_precedence_cautious.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('auraria_tau_cautious_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

precedence=np.genfromtxt("auraria_tau_precedence_risky.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('auraria_tau_risky_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

# City Park
s=834

precedence=np.genfromtxt("citypark_tau_precedence_cautious.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('citypark_tau_cautious_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

precedence=np.genfromtxt("citypark_tau_precedence_risky.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('citypark_tau_risky_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

# DU
s=427

precedence=np.genfromtxt("DU_tau_precedence_cautious.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('DU_tau_cautious_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

precedence=np.genfromtxt("DU_tau_precedence_risky.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('DU_tau_risky_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

# Union
s=433

precedence=np.genfromtxt("union_tau_precedence_cautious.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('union_tau_cautious_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

precedence=np.genfromtxt("union_tau_precedence_risky.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('union_tau_risky_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

# 5points
s=112

precedence=np.genfromtxt("5points_tau_precedence_cautious.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('5points_tau_cautious_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

precedence=np.genfromtxt("5points_tau_precedence_risky.csv", delimiter=",")
paths = generate_paths(s, edges, precedence)

with open('5points_tau_risky_paths.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(paths)

