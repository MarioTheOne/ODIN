import community


def get_partition_from_modularity_att(graph):
    partition = {}

    for node in graph.node.values():
        partition[node['label']] = node['Modularity Class']

    return partition


def louvain(graph):
    partition = community.best_partition(graph)
    return __get_communities_from_partition__(partition)


def __get_louvain_best_partition(graph):
    result = community.best_partition(graph)
    return result


def __get_communities_from_partition__(partition):
    communities = {}
    for k, v in partition.items():
        if v in communities:
            communities[v].append(k)
        else:
            communities[v] = [k]
    return communities


def louvain_community_detection(undirected_graph):
    partition = community.best_partition(undirected_graph)
    communities = __get_communities_from_partition__(partition)
    return communities, partition
