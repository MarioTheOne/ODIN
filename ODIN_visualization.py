import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os


def plot_auc(false_positive_rates, true_positive_rates):
    plt.figure()
    plt.plot(false_positive_rates, true_positive_rates, 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


def draw_graph_communities(graph, partition):
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(graph)
    count = 0.
    for com in set(partition.values()):
        count += 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(graph, pos, list_nodes, node_size=20,
                               node_color=str(count / size))

    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    plt.show()


def draw_graph(graph):
    nx.draw(graph, pos=nx.spring_layout(graph))
    plt.show()


def draw_graph_with_anomalies(graph, anomaly_list):
    node_colors = []
    for node in nx.nodes(graph):
        if node in anomaly_list:
            node_colors.append('red')
        else:
            node_colors.append('cyan')

    nx.draw(graph, node_color=node_colors, pos=nx.spring_layout(graph))
    plt.show()


def save_histogram_file(file_name, save_path, data_dict, x_label, y_label, title):
    y_list = []
    x_list = []

    for k, v in data_dict.items():
        x_list.append(k)
        y_list.append(v)

    y = np.array(y_list)

    plt.bar(np.arange(len(x_list)), y)
    plt.xticks(np.arange(len(x_list)), x_list)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(os.path.join(save_path, file_name))
    plt.show()
    plt.close()
