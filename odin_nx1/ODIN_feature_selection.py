import numpy as np
import skfeature.function.similarity_based.lap_score as lap_score
import skfeature.function.similarity_based.SPEC as SPEC
from skfeature.utility.construct_W import construct_W


def laplacian_score(graph, community, att_names, percentile):
    community_as_matrix = np.empty((len(community), len(att_names)))
    for instance_number in range(0, len(community)):
        instance_id = community[instance_number]
        instance = graph.node[instance_id]
        for att_number in range(0, len(att_names)):
            community_as_matrix[instance_number, att_number] = instance[att_names[att_number]]

    # This is a workaround for avoiding a crash for the problem with k of knn in the library construct_W
    # If the problem is not solved soon I should implement my own function instead of the workaround
    W = None
    if len(community) >= 5:
        W = construct_W(community_as_matrix)
    else:
        W = construct_W(community_as_matrix, k=(len(community) - 1))

    scores = lap_score.lap_score(community_as_matrix, W=W)

    ranked_att = lap_score.feature_ranking(scores)

    result = []
    boundary = len(att_names)*percentile
    for i in range(0, len(att_names)):
        if ranked_att[i] < boundary:
            result.append(att_names[i])

    return result


def spec(graph, community, att_names, percentile):
    community_as_matrix = np.empty((len(community), len(att_names)))
    for instance_number in range(0, len(community)):
        instance_id = community[instance_number]
        instance = graph.node[instance_id]
        for att_number in range(0, len(att_names)):
            community_as_matrix[instance_number, att_number] = instance[att_names[att_number]]

    # This is a workaround for avoiding a crash for the problem with k of knn in the library construct_W
    # If the problem is not solved soon I should implement my own function instead of the workaround
    W = None
    if len(community) >= 5:
        W = construct_W(community_as_matrix)
    else:
        W = construct_W(community_as_matrix, k=(len(community) - 1))

    scores = SPEC.spec(community_as_matrix, W=W)

    ranked_att = lap_score.feature_ranking(scores)

    result = []
    boundary = len(att_names)*percentile
    for i in range(0, len(att_names)):
        if ranked_att[i] < boundary:
            result.append(att_names[i])

    return result
