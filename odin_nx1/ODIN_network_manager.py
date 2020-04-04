# This module is in charge of managing the network representations

import networkx as nx
import pickle
# from copy import deepcopy


def write_network_as_gpickle_file(network, file_path):
    nx.write_gpickle(network, file_path)


def read_network_from_gpickle_file(file_path):
    result = nx.read_gpickle(file_path)
    return result


def write_dictionary_as_pickle_file(dictionary, file_path):
    with open(file_path, 'wb') as file_handle:
        pickle.dump(dictionary, file_handle, pickle.HIGHEST_PROTOCOL)


def read_dictionary_from_pickle_file(file_path):
    with open(file_path, 'rb') as file_handle:
        return pickle.load(file_handle)

# def get_underlaying_undirected_graph(directed_graph):
#     directed_graph = nx.DiGraph()
#
#     result = nx.Graph()
#     result.name = directed_graph.name
#     result.add_nodes_from(directed_graph)
#
#     for edge in directed_graph.edges():
#
#
#     result.add_edges_from((u, v, deepcopy(d))
#                      for u, nbrs in directed_graph.adjacency_iter()
#                      for v, d in nbrs.items())
#
#     result.graph = deepcopy(directed_graph.graph)
#     result.node = deepcopy(directed_graph.node)
#     return result
