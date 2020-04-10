# This module contains the functions for building a network from tweets
import json
import networkx as nx
import os
import io


def read_retweet_network(tweets_folder_path):
    # creating an empty graph
    graph = nx.DiGraph()

    # reading all the tweets in the given folder
    for file_name in os.listdir(tweets_folder_path):
        # open the json file of the tweet
        json_tweet = io.open(file=tweets_folder_path + '\\' + file_name, mode='r', encoding='utf-8')
        tweet = json.load(json_tweet)

        # if the tweet is a retweet then it is processed
        if 'retweeted_status' in tweet:
            user_retweeter_id = tweet['user']['id_str']
            user_retweeter_screen_name = tweet['user']['screen_name']
            user_retweeted_id = tweet['retweeted_status']['user']['id_str']
            user_retweeted__screen_name = tweet['retweeted_status']['user']['screen_name']

            # if the retweeter user is not in graph then add it
            if user_retweeter_id not in graph.nodes:
                graph.add_node(user_retweeter_id, attr_dict={'screen_name': user_retweeter_screen_name})

            # if the retweeted user is not in graph then add it
            if user_retweeted_id not in graph.nodes:
                graph.add_node(user_retweeted_id, attr_dict={'screen_name': user_retweeted__screen_name})

            # if there is a previous relationship between the users, increase its count
            if graph.has_edge(user_retweeter_id, user_retweeted_id):
                edge_data = graph[user_retweeter_id][user_retweeted_id]
                edge_data['count'] += 1
            else:
                # if there's not a previous relationship then add an edge
                # edge_atts = {'count': 1}
                graph.add_edge(user_retweeter_id, user_retweeted_id, count=1)

        json_tweet.close()

    return graph


def get_out_degree_per_vertex(graph):
    degrees = graph.out_degree(weight='count')
    node_degree_dict = dict(degrees)
    return node_degree_dict


def get_in_degree_per_vertex(graph):
    degrees = graph.in_degree(weight='count')
    node_degree_dict = dict(degrees)
    return node_degree_dict


def get_degree_per_vertex(graph):
    degrees = graph.degree(weight='count')
    node_degree_dict = dict(degrees)
    return node_degree_dict


def get_inter_links_degree_per_vertex(graph, partition):
    node_degree_dict = {}
    node_in_degree_dict = {}
    node_out_degree_dict = {}

    for node in graph.nodes():
        in_inter_community_links = 0
        out_inter_community_links = 0

        node_com = partition[node]

        # iterating over in edges
        for u_from_in, u_to_in, edge_atts_in in graph.in_edges(node, data=True):
            # if the source node has a different community from the destiny node
            if partition[u_from_in] != node_com:
                # Adding the total number of links with external users
                in_inter_community_links += edge_atts_in['count']

        # iterating over out edges
        for u_from_out, u_to_out, edge_atts_out in graph.out_edges(node, data=True):
            # if the destiny node has a different community from the source node
            if partition[u_to_out] != node_com:
                # Adding the total number of links with external users
                out_inter_community_links += edge_atts_out['count']

        node_degree_dict[node] = in_inter_community_links + out_inter_community_links
        node_in_degree_dict[node] = in_inter_community_links
        node_out_degree_dict[node] = out_inter_community_links

    return node_degree_dict, node_in_degree_dict, node_out_degree_dict
