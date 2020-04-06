import math as math


# Assigns an outlierness score to each element using normal distribution
# Parameters: data_dict a dictionary containing (element_id, value)
# Output: A dictionary containing for each element its outlierness score
def gaussian_score(data_dict):
    result = {}

    # Calculating mean
    mean = 0
    for v in data_dict.values():
        mean += v
    mean = mean/len(data_dict)

    # Calculating variance
    variance = 0
    for v in data_dict.values():
        variance += math.pow(v-mean, 2)
    variance = variance/len(data_dict)

    # Calculating the score
    for k, v in data_dict.items():
        # Calculating normality score
        exp = -(math.pow(v-mean, 2)/(2*variance))
        k_norm_score = (1/(math.sqrt(variance)*math.sqrt(2*math.pi)))*(math.pow(math.e, exp))

        # Calculating outlierness score
        k_outlierness_score = 1/(1 + k_norm_score)

        # Storing the result
        result[k] = k_outlierness_score

    # returning the score
    return result


# Assigns an outlierness score to graph vertices based on their out-degree
def out_degree_gaussian_anomalies(graph):
    node_degree_dict = {}
    for node in graph.nodes():
        node_out_degree = 0

        for u_from, u_to, edge_atts in graph.out_edges(node, data=True):
            node_out_degree += edge_atts['count']

        node_degree_dict[node] = node_out_degree

    return gaussian_score(node_degree_dict)


# Assigns an outlierness score to graph vertices based on their in-degree
def in_degree_gaussian_anomalies(graph):
    node_degree_dict = {}
    for node in graph.nodes():
        node_in_degree = 0

        for u_from, u_to, edge_atts in graph.in_edges(node, data=True):
            node_in_degree += edge_atts['count']

        node_degree_dict[node] = node_in_degree

    return gaussian_score(node_degree_dict)


# the name stands for Directed Signed InterScore. Ranks elements according to their number of
# inter-community out/in edges compared to their community mean. This algorithm can be used to
# identify users open mindedness/influence in re-tweet networks.
# Parameters:
# graph - A directed graph representing the network
# communities - A dictionary containing for each community_id a list of the vertices belonging to it
# partition - A dictionary containing for each node_id to which community it belongs
# in_edge_analysis - if true, only the in-edges are analyzed, else only the out-edges are analyzed
# negative_anomalies - if false, the algorithm considers only those elements anomalous because their
#                      attribute value is greater than the common range for their community
# Output:
# A dict containing for each node_id its outlierness score
def inter_score_ds(graph, communities, partition, in_edges_analysis=False, negative_anomalies=False):
    outlier_ranking = {}

    # iterate over each community
    for community in communities.values():
        vertex_intercommunity_links = {}
        community_size = len(community)

        # calculating the inter-community links of each vertex inside the community
        if in_edges_analysis:
            for v in community:
                inter_community_links = 0
                v_com = partition[v]

                # iterating over in edges
                for u_from, u_to, edge_atts in graph.in_edges(v, data=True):
                    # if the source node has a different community from the destiny node
                    if partition[u_from] != v_com:
                        # Adding the total number of links with external users
                        inter_community_links += edge_atts['count']

                vertex_intercommunity_links[v] = inter_community_links
        else:
            for v in community:
                inter_community_links = 0
                v_com = partition[v]

                # iterating over out edges
                for u_from, u_to, edge_atts in graph.out_edges(v, data=True):
                    # if the destiny node has a different community from the source node
                    if partition[u_to] != v_com:
                        # Adding the total number of links with external users
                        inter_community_links += edge_atts['count']

                vertex_intercommunity_links[v] = inter_community_links

        # calculating the mean inter-community-links dissimilarity in the community
        mean_inter_community_link_difference = 0.0
        pair_count = 0
        for v_i in range(0, len(community) - 1):
            for v_j in range(v_i + 1, len(community)):
                pair_count += 1
                pair_diff = abs(vertex_intercommunity_links[community[v_i]] -
                                vertex_intercommunity_links[community[v_j]])
                mean_inter_community_link_difference += float(pair_diff)

        # in the case the community has only a vertex, the mean dissimilarity is 0
        if pair_count > 0:
            mean_inter_community_link_difference /= float(pair_count)

        # calculating the outlierness score of each vertex
        if negative_anomalies:
            # iterate over each vertex v in the community
            for v in community:
                v_score = 0.0
                # iterate over the other members v_2 of its community
                for v_2 in community:
                    if v != v_2:
                        # Determine if difference between v and its group members is greater than the mean difference
                        signed_difference = vertex_intercommunity_links[v] - vertex_intercommunity_links[v_2]
                        link_dissimilarity = abs(signed_difference)
                        if link_dissimilarity > mean_inter_community_link_difference and signed_difference < 0:
                            v_score += 1.0

                v_score /= float(community_size)

                # saving the score into the ranking
                outlier_ranking[v] = v_score
        else:
            # iterate over each vertex v in the community
            for v in community:
                v_score = 0.0
                # iterate over the other members v_2 of its community
                for v_2 in community:
                    if v != v_2:
                        # Determine if difference between v and its group members is greater than the mean difference
                        signed_difference = vertex_intercommunity_links[v] - vertex_intercommunity_links[v_2]
                        link_dissimilarity = abs(signed_difference)
                        if link_dissimilarity > mean_inter_community_link_difference and signed_difference >= 0:
                            v_score += 1.0

                v_score /= float(community_size)

                # saving the score into the ranking
                outlier_ranking[v] = v_score

    return outlier_ranking


# The glance score function assigns to each node a value indicating how anomalous it is compared
# to the members of its same community. Each node have an attributes vector.
# Parameters:
# graph - An undirected graph with attributed nodes representing the network
# communities - A dictionary containing for each community_id a list of the vertices belonging to it
# att_to_analyze - A list with the names of the node attributes to use in the analysis
# Output:
# A dict containing for each node_id its outlierness score
def glance(graph, communities, att_to_analyze):
    # The list of the detected anomalies
    result = {}

    # Iterate over the communities of the graph
    for community in communities.values():

        # Calculate the mean difference among elements
        dcount = 0
        dmean = {}
        for att in att_to_analyze:
            dmean[att] = 0

        for v1_id in community:
            for v2_id in community:
                if v2_id != v1_id:
                    for att in att_to_analyze:
                        dmean[att] += math.fabs(graph.node[v1_id][att] - graph.node[v2_id][att])
                dcount += 1

        for att in dmean:
            dmean[att] = dmean[att]/dcount

        # Iterate over the community vertices
        for v1_id in community:
            att_diff = {}
            for v2_id in community:
                if v1_id != v2_id:

                    # Getting a dictionary indicating which attributes from v1 are very different from the ones in v2
                    v1_v2_diff = {}
                    for att in att_to_analyze:
                        if math.fabs(graph.node[v1_id][att] - graph.node[v2_id][att]) > dmean[att]:
                            v1_v2_diff[att] = 1
                        else:
                            v1_v2_diff[att] = 0

                    # Storing from how many vertices in v1's community is different each att from v1
                    if att_diff:
                        for att_k, att_v in v1_v2_diff.items():
                            att_diff[att_k] += att_v
                    else:
                        att_diff = v1_v2_diff

            # Calculate the outlierness score for the node
            v1_outlierness_score = 0
            for result_k, result_v in att_diff.items():
                temp_score = float(result_v)/float(len(community))
                if temp_score > v1_outlierness_score:
                    v1_outlierness_score = temp_score
            result[v1_id] = v1_outlierness_score

    return result


# Algorithm proposed by
# Hellig et al. 2019. A Community-Aware Approach for Identifying Node Anomalies in Complex Networks
# Parameters:
# graph - A directed graph representing the network
# partition - A dictionary containing for each node_id to which community it belongs
# Output:
# A dict containing for each node_id its outlierness score
def cada(graph, partition):
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
