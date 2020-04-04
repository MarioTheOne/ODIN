from odin_nx1 import ODIN_network_manager as net_manager, ODIN_twitter_network_manager as tw_manager

print('Welcome to project ODIN! this project is currently under development. It will become more stable with time ;)')

#us_elections_2018_retweets = \
#    net_manager.read_network_from_gpickle_file('Networks/us_elections_2018_retweets/us_elections_retweets.gpickle')


DiG = tw_manager.read_retweet_network('D:/Work/Databases/Tweets/EleccionesEEUU/Tweets')

net_manager.write_network_as_gpickle_file(DiG, 'us_elections_2018_retweets')


