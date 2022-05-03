# Bike Map Preprocessing

library(sfnetworks)
library(sf)
library(tidygraph)
library(tidyverse)
library(igraph)
library(dbscan)
library(sp)

# load data
data <- st_read("desktop/official-city-of-denver-bike-map/bike_lanes.shp")

edges <- st_as_sf(data, crs = 4326)

# Force Overlap

st_geometry(edges) = st_geometry(edges) %>%
  lapply(function(x) round(x,4)) %>%
  st_sfc(crs = st_crs(edges))

# The edges are connected.
net = as_sfnetwork(edges)

plot(st_geometry(net, "edges"), col = blues9, lwd = 4)
plot(st_geometry(net, "nodes"), pch = 20, cex = 1.5, add = TRUE)

# Delete loops, multiple edges
simple = net %>%
  activate("edges") %>%
  filter(!edge_is_multiple()) %>%
  filter(!edge_is_loop())

plot(st_geometry(simple, "edges"), col = blues9, lwd = 4)
plot(st_geometry(simple, "nodes"), pch = 20, cex = 1.5, add = TRUE)


# Subdivide edges
subdivision = convert(simple, to_spatial_subdivision)
plot(st_geometry(subdivision, "edges"), col = blues9, lwd = 4)
plot(st_geometry(subdivision, "nodes"), pch = 20, cex = 1.5, add = TRUE)


# Check connected components
with_graph(subdivision, graph_component_count())

# Returns 74
# Take largest connected component (includes 2/3 of nodes)

connected_net = subdivision %>%
  activate("nodes") %>%
  filter(group_components() == 1)

plot(connected_net, cex = 1.1, lwd = 1.1)


# Delete Redundant Nodes
smoothed = convert(connected_net, to_spatial_smooth)
plot(st_geometry(smoothed, "edges"), col = blues9, lwd = 4)
plot(st_geometry(smoothed, "nodes"), pch = 20, cex = 1.1, add = TRUE)


# Get edge info and export
my_edges = st_as_sf(smoothed, "edges")
edges_df = data.frame(my_edges$from, my_edges$to, my_edges$EXISTING_F, my_edges$FULLNAME,
                      my_edges$FROMNAME, my_edges$TONAME)

write.csv(edges_df, "desktop/cleaned_edges.csv", row.names = FALSE)

# Get node info and export
my_coords = smoothed %>%
  activate("nodes") %>%
  st_coordinates()

write.csv(my_coords, "desktop/cleaned_coords.csv", row.names = FALSE)



