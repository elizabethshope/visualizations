# Libraries
library(igraph)
library(networkD3)

# Read in and clean up data
tribeEdges <- read.table('soc-tribes.edges', skip=2)
tribeEdges <- tribes[order(tribeEdges$V1, tribeEdges$V2),]
rownames(tribeEdges) <- NULL
colnames(tribeEdges) <- c("From", "To", "Weight")
tribeEdges$Weight <- sapply(tribeEdges$Weight, function(x) ifelse(x == 1, 1, 0))
tribeEdges$SourceID <- tribeEdges$From - 1
tribeEdges$TargetID <- tribeEdges$To - 1

tribeNodes <- read.csv("tribeNames.csv", stringsAsFactors = FALSE)

# Create igraph
g <- igraph::graph_from_data_frame(tribeEdges, directed = FALSE, vertices = tribeNodes)

# Add group to nodes (we are going to have all nodes be in the same group)
tribeNodes$Group <- rep(1, 16)

# Calculate degree for all nodes & add to node list
tribeNodes <- cbind(tribeNodes, nodeDegree=igraph::degree(g, v = igraph::V(g),mode = "all"))

# Calculate betweenness for all nodes
betAll <- igraph::betweenness(g, v = igraph::V(g), directed = FALSE) / 
  (((igraph::vcount(g) - 1) * (igraph::vcount(g)-2)) / 2)
betAll.norm <- (betAll - min(betAll))/(max(betAll) - min(betAll))
tribeNodes <- cbind(tribeNodes, nodeBetweenness=100*betAll.norm) # We are scaling the value by multiplying it by 100 for visualization purposes only (to create larger nodes)
rm(betAll, betAll.norm)

# Set edge colors & color mapping for nodes
edges_col <- sapply(tribeEdges$Weight, function(x) ifelse(x == 1, "#67cc66", "#ff6860"))
ColourScale <- 'd3.scaleOrdinal().domain([1]).range(["black"]);'

# Create force network
D3_network_tribes <- forceNetwork(Links = tribeEdges, 
                                  Nodes = tribeNodes, 
                                  Source = 'SourceID', 
                                  Target = 'TargetID', 
                                  NodeID = 'name', 
                                  Group = 'Group',
                                  Nodesize = 'nodeBetweenness',
                                  linkDistance = 200,
                                  linkWidth = 2,
                                  charge = -200,
                                  fontSize = 25,
                                  opacity = 0.8,
                                  opacityNoHover = 0.6,
                                  linkColour = edges_col,
                                  colourScale = networkD3::JS(ColourScale))

# Save network as html file
networkD3::saveNetwork(D3_network_tribes, "tribes_networkD3.html", selfcontained = TRUE)

