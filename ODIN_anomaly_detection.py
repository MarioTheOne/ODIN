import math as math



def out_inter_score(graph, communities, partition):
    outlier_ranking = dict()

    # iterate over each community
    for community in communities.values():
        vertex_intercommunity_links = {}
        community_size = len(community)

        # calculating the inter-community links of each vertex inside the community
        for v in community:
            inter_community_links = 0
            v_com = partition[v]

            for u_from, u_to, edge_atts in graph.out_edges(v, data=True):
                if partition[u_to] != v_com:
                    # Adding the total number of link with external users
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
        for v in community:
            v_score = 0.0
            for v_2 in community:
                if v != v_2:
                    link_dissimilarity = abs(vertex_intercommunity_links[v] - vertex_intercommunity_links[v_2])
                    if link_dissimilarity > mean_inter_community_link_difference:
                        v_score += 1.0

            v_score /= float(community_size)

            # saving the score into the ranking
            outlier_ranking[v] = v_score

    return outlier_ranking


# Assigns an outlierness score to each element using normal distribution
def gaussian(data_dict):
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


def out_degree_gaussian_anomalies(graph):
    node_degree_dict = {}
    for node in graph.nodes():
        node_out_degree = 0

        for u_from, u_to, edge_atts in graph.out_edges(node, data=True):
            node_out_degree += edge_atts['count']

        node_degree_dict[node] = node_out_degree

    return gaussian(node_degree_dict)


def in_degree_gaussian_anomalies(graph):
    node_degree_dict = {}
    for node in graph.nodes():
        node_out_degree = 0

        for u_from, u_to, edge_atts in graph.in_edges(node, data=True):
            node_out_degree += edge_atts['count']

        node_degree_dict[node] = node_out_degree

    return gaussian(node_degree_dict)


# the name stands for Directed Signed InterScore. Ranks the elements according to their number of
# inter-community out/in edges compared to their community mean. This algorithm can be used to
# identify user open mindedness/influence in re-tweet networks.
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
