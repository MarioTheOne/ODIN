from odin_core import ODIN_network_manager as NetManager
from odin_core import ODIN_twitter_network_manager as TwManager
from odin_core import ODIN_graph_clustering as Gclust
from odin_core import ODIN_anomaly_detection as AnDet

print('Welcome to project ODIN!')
print('This project offers a set of functions to perform Anomaly Detection on Complex Networks')
print('To see how to use the functions to perform anomaly detection see the provided Jupyter Notebooks')

print('The project is currently under development. It will become more stable with time ;)')

database_path = 'D:/Work/Databases/Dynamic Networks/DBLP CoAuth/coauth-DBLP/'
simplices_file = database_path + 'coauth-DBLP-simplices.txt'
nvert_file = database_path + 'coauth-DBLP-nverts.txt'
times_file = database_path + 'coauth-DBLP-times.txt'
vertices_names_file = database_path + 'coauth-DBLP-node-labels.txt'

# dblp_network_2013 = NetManager.read_snapshot_from_simplices(simplices_file, nvert_file, times_file,
#                                                               vertices_names_file, 2013)
#
# NetManager.write_network_as_gpickle_file(dblp_network_2013, 'Networks/dblp/dblp_network_2013.gpickle')

