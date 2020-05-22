import pandas as pd
import numpy as np
from sklearn import preprocessing
import math

def clustering_mean_prices(dataset):
	"""This function gets the results, calculate the mean prices for each cluster, and returns a dataframe of results
	that will be used to determine the best cluster (or closest cluster)"""
	results = dataset.loc[:,['modelo_celular','menor_preco','link_anuncio','cluster']]
	clusters = results.groupby(by='cluster').mean().reset_index()

	# add cluster mean to the results
	cluster_mean_price = {}
	n_clusters = len(results.loc[:,'cluster'].unique())
	for cluster in list(np.arange(n_clusters)+1):
		cluster_mean_price[cluster] = round(clusters.loc[clusters.loc[:,'cluster'] == cluster].loc[:,'menor_preco'].values[0],2)

	# adding mean price for each cluster
	results['c_mean_price'] = results.loc[:,'cluster'].apply(lambda x: cluster_mean_price[x])

	return results

def winner_cluster(results, usr):
	"""This function receives the results dataframe and the user input (usr) and returns the cluster with closest mean prices to the user input."""

	#check closest cluster
	temp_df = results.copy()

	temp_df['cluster_dist'] = temp_df.loc[:,'c_mean_price'].apply(lambda x: math.sqrt((x-usr)**2))

	#separate this cluster
	closest_cluster = temp_df.loc[temp_df['cluster_dist'] == temp_df['cluster_dist'].min()]

	#get winner smartphone (closest)

	closest_cluster['phone_dist'] = closest_cluster.loc[:,'menor_preco'].apply(lambda x: math.sqrt((x-usr)**2))

	winner = closest_cluster.loc[closest_cluster.phone_dist == closest_cluster.phone_dist.min()]

	return winner


def select_winner(main_data, winner):
	"""This function receives the winner dataframe, and select the winner (or best) smartphone and returns the url and price of the best smartphone."""

	if winner.shape[0] >1:
		#Get complete data from winners and filter numeric properties
		colunas_de_desempate = ['data_anuncio', 'tela', '4g', '3g','camera traseira', 'camera selfie', 'nfc', 'memoria interna']
		temp_df = main_data.copy().loc[list(winner.index)].loc[:, colunas_de_desempate]
		temp_df = temp_df.loc[:,~(temp_df.dtypes == object)].drop_duplicates()

		# add score at the end of each df
		x = temp_df.values #returns a numpy array
		min_max_scaler = preprocessing.MinMaxScaler()
		x_scaled = min_max_scaler.fit_transform(x)
		temp_df['score'] = pd.DataFrame(x_scaled).sum(axis=1).values

		# filter winner
		winnerindex = temp_df.loc[temp_df.loc[:,'score'] == temp_df.loc[:,'score'].max()].index
		winner = main_data.loc[winnerindex]

	winner_url, winner_price = winner.link_anuncio.values[0], winner.menor_preco.values[0]
	return winner_url, winner_price

def get_my_smartphone(dataset, money, upper=1.2):
	"""This function receives the labeled dataset, an amount of money and returns
	a list of the best fit device's url and price, as well as the url and price
	from a suggested smartphone. The upper"""
	results = clustering_mean_prices(dataset)

	#base
	winner = winner_cluster(results=results, usr=money)
	choosen_url, choosen_price = select_winner(main_data=dataset, winner=winner)

	#upper suggestion
	suggestion = winner_cluster(results=results, usr=money*upper)
	# get the suggested smartphone
	suggestion_url, suggestion_price = select_winner(main_data=dataset, winner=suggestion)
	return [choosen_url, choosen_price, suggestion_url, suggestion_price]