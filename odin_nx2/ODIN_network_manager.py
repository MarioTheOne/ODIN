# This module is in charge of managing the network representations
import networkx as nx
import pickle


def write_network_as_gpickle_file(network, file_path):
    nx.write_gpickle(network, file_path)


def read_network_from_gpickle_file(file_path):
    result = nx.read_gpickle(file_path)
    return result


def read_network_from_graphml(file_path):
    result = nx.read_graphml(file_path)
    return result


def write_dictionary_as_pickle_file(dictionary, file_path):
    with open(file_path, 'wb') as file_handle:
        pickle.dump(dictionary, file_handle, pickle.HIGHEST_PROTOCOL)


def read_dictionary_from_pickle_file(file_path):
    with open(file_path, 'rb') as file_handle:
        return pickle.load(file_handle)
