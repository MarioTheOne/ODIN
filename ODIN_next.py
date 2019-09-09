import networkx as nx
from community import community_louvain


# Algorithm proposed by
# Hellig et al. 2019. A Community-Aware Approach for Identifying Node Anomalies in Complex Networks
def CADA(graph, partition):
    result = {}
    # Iterate over all vertices of the graph
    for v in graph.nodes():
        # For each vertex iterate over its neighbors
        neighbors_dict = {}
        for neighbor in graph.neighbors(v):
            # record the amount of neighbors belonging to each partition
            n_com = partition[neighbor]

            if n_com in neighbors_dict:
                neighbors_dict[n_com] += 1
            else:
                neighbors_dict[n_com] = 1

        # Sum the total neighbors of the node and divide that for the max number of neighbors in the same community
        max_neighbors_in_community = 0
        outlierness_score = 0
        for val in neighbors_dict.values():
            if max_neighbors_in_community < val:
                max_neighbors_in_community = val

            outlierness_score += val

        outlierness_score = outlierness_score/max_neighbors_in_community

        # Save the outlierness score for the node
        result[v] = outlierness_score

    return result


def Test_CADA_on_Disney():
    graph = nx.read_graphml('Databases//Disney.graphml')
    partition = community_louvain.best_partition(graph)

    outlierness_score = CADA(graph, partition)

    return outlierness_score



outlierness_score = Test_CADA_on_Disney()
print(outlierness_score)




