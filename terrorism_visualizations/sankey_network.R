# Imports
library(networkD3)
library(igraph)

### THIS IS THE CODE FOR CREATING THE NODE AND EDGE LISTS AND SAVING THEM TO CSV
### I HAVE COMMENTED THIS OUT AND AM JUST IMPORTING THE CSVS THAT I CREATED

# # Read in data
# data <- "../../../Downloads/TerrorismDATA_Real_1970_2016.csv"
# terrorism <- read.csv(data, header=TRUE, skip=2)
# 
# # Create edge list
# edgeList <- data.frame(table(terrorism$region_txt, terrorism$attacktype1_txt))
# colnames(edgeList) <- c("From", "To", "Weight")
# 
# # Create node list
# region_nodes <- as.integer(unique(edgeList$From))
# names(region_nodes) <- levels(unique(edgeList$From))
# region_nodes <- region_nodes - 1
# attack_nodes <- as.integer(unique(edgeList$To))
# names(attack_nodes) <- levels(unique(edgeList$To))
# attack_nodes <- attack_nodes + 11
# nodeList <- data.frame("ID" = c(region_nodes, attack_nodes))
# nodeList$Name <- rownames(nodeList)
# rownames(nodeList) <- NULL
# nodeList <- nodeList[c("Name", "ID")]
# 
# # Save node and edge lists to CSV
# write.csv(nodeList, "NodeList.csv", row.names = FALSE)
# write.csv(edgeList, "EdgeList.csv", row.names = FALSE)

# Import node and edge lists
nodeList <- read.csv("NodeList.csv", header = TRUE)
edgeList <- read.csv("EdgeList.csv", header = TRUE)

# Create graph
g <- graph_from_data_frame(edgeList, directed=TRUE, vertices=nodeList)
terrorism_d3 <- igraph_to_networkD3(g)

ColourScale <- 'd3.scaleOrdinal(d3.schemeCategory10);'

# NodeGroup = factor(terrorism_d3$nodes$group),
terrorism_network <- sankeyNetwork(Links = terrorism_d3$links, Nodes = terrorism_d3$nodes, Source = "source",
                                   Target = "target", Value = "value", NodeID = "name",
                                   units = "Incidents", fontSize = 12, nodeWidth = 30,
                                   colourScale = networkD3::JS(ColourScale))

networkD3::saveNetwork(terrorism_network, "terrorism_network.html", selfcontained = TRUE)
