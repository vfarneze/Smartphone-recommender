from datetime import datetime
import os

class Params:
	"""
	Parameters for the jacotei extraction pipeline.
	"""
	#
	raw_data = '../data_storage/raw/jctraw' + datetime.now().strftime("%Y-%m-%d") + '.csv'
	trans_data = '../data_storage/transformed/jcttreated' + datetime.now().strftime("%Y-%m-%d") + '.csv'
	temp_data = '../data_storage/temp/toDB' + datetime.now().strftime("%Y-%m-%d") + '.csv'
	db_data = '../data_storage/dblogs/dblog' + datetime.now().strftime("%Y-%m-%d") + '.csv'

	## Database connection params
	user = 'postgres'
	password = '123qweasd'
	host = 'localhost'
	database = 'Smartphones-DB'

	#Info specific about webscrapping
	force_execution = False

	#log_folder = r"C:\Users\vFarn\Documents\ironhack\personal_projs\phone-price-tracker\log"


	# parameters for data_extraction
	page=1
	number_per_page=10000
	url = 'https://www.jacotei.com.br/busca/?cids=57&bids=&fids=&o=2' +  f'&p={page}' + f'&n={number_per_page}'
	backup_folder= r"C:\Users\vFarn\Documents\ironhack\personal_projs\phone-price-tracker\data_storage\backup_folder\backup_df.csv"


	#parameters for data_storage
	postgres_db = f'postgresql+psycopg2://{user}:{password}@localhost/{database}'
	prefix=r'jct_data_'
	database_name='jct' + datetime.now().strftime("%Y-%m-%d")
	#storagepath = r"C:\Users\vFarn\Documents\ironhack\personal_projs\phone-price-tracker\data_storage\jct_data_"