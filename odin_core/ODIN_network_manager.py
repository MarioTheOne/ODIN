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


def read_dynamic_network_from_simplices(simplices_file, nvert_per_simplex_file, simplices_time_file,
                                        vertices_labels_file):
    # Open all the files
    simplices_f = open(simplices_file, 'r')
    nvert_f = open(nvert_per_simplex_file, 'r')
    times_f = open(simplices_time_file, 'r')

    node_labels_dict = __read_labels_dict__(vertices_labels_file)

    # Create the dynamic graph to return
    dynamic_graph = {}

    # Iterate over the file containing the sizes of the simplices
    for nv_line in nvert_f:
        # Get the number of vertices and the timestamp of the simplex
        nvert = int(nv_line.rstrip('\n'))
        timestamp = int(times_f.readline().rstrip('\n'))

        # If the timestamp is not yet in the graph then create a new snapshot
        if timestamp not in dynamic_graph:
            dynamic_graph[timestamp] = nx.Graph()

        # Get the simplex
        vlist = []
        for i in range(0, nvert):
            vlist.append(int(simplices_f.readline().rstrip('\n')))

        # Add the simplex to the graph
        __add_clique__(dynamic_graph[timestamp], vlist, node_labels_dict)

    # Close the file handlers
    simplices_f.close()
    nvert_f.close()
    times_f.close()

    # Return the dynamic network
    return dynamic_graph


def read_snapshot_from_simplices(simplices_file, nvert_per_simplex_file, simplices_timestamps_file,
                                 vertices_labels_file, filter_timestamp):
    # Open all the files
    simplices_f = open(simplices_file, 'r')
    nvert_f = open(nvert_per_simplex_file, 'r')
    times_f = open(simplices_timestamps_file, 'r')

    node_labels_dict = __read_labels_dict__(vertices_labels_file)

    # Create the dynamic graph to return
    result = nx.Graph()

    # Iterate over the file containing the sizes of the simplices
    for nv_line in nvert_f:
        # Get the timestamp of the simplex
        timestamp = int(times_f.readline().rstrip('\n'))

        # If the timestamp match the filter timestamp
        if timestamp == filter_timestamp:
            # Get the number of vertices in the simplex
            nvert = int(nv_line.rstrip('\n'))

            # Get the simplex
            vlist = []
            for i in range(0, nvert):
                vlist.append(int(simplices_f.readline().rstrip('\n')))

            # Add the simplex to the graph
            __add_clique__(result, vlist, node_labels_dict)

    # Close the file handlers
    simplices_f.close()
    nvert_f.close()
    times_f.close()

    # Return the dynamic network
    return result


def get_matching_nodes_percent(graph_1, graph_2):
    matching_nodes = 0
    for n in graph_1.nodes:
        if n in graph_2.nodes:
            matching_nodes += 1

    return matching_nodes / (len(graph_1.nodes) + len(graph_2.nodes) - matching_nodes)


def __read_labels_dict__(vertices_labels_file):
    # Open the labels file
    labels_f = open(vertices_labels_file, 'r')

    # Create the empty dict to return
    result = {}

    # Iterate over the lines of the label file and parse the pairs (node_id, label)
    for line in labels_f:
        list_line = line.split(' ', 1)
        result[int(list_line[0])] = list_line[1].rstrip('\n')

    labels_f.close()
    return result


def __add_clique__(graph, vlist, label_dict):
    # Add to the graph the nodes that does not exist already
    for v in vlist:
        if not graph.has_node(v):
            graph.add_node(v, attr_dict={'label': label_dict[v]})  # Add the label to the node

    # Add edges among all nodes of the list
    for v_i in range(0, len(vlist)):
        for v_j in range(v_i+1, len(vlist)):
            # if the edge already exists then increase its count att
            if graph.has_edge(vlist[v_i], vlist[v_j]):
                edge_data = graph[vlist[v_i]][vlist[v_j]]
                edge_data['count'] += 1
            # Create the new edge with count attribute in 1
            else:
                graph.add_edge(vlist[v_i], vlist[v_j], count=1)

