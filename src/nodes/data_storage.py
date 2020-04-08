import logging
import pandas as pd
from sqlalchemy import create_engine
import os


def done(client,params):
	'''Returns true there is data extracted today'''
	if os.path.isfile(params.db_data):
		print('>>>> Already runned data_stored today... (3/3)')
		return True

	else:
		return False

def update(client,params):
	'''	This function saves a stores the pipeline dataframe in a database.'''
	df = pd.read_csv(params.temp_data, encoding='cp1252')

	df.to_sql(params.table_name, client.conn, index=False, if_exists='append')

	#Since i am the only one with access to the database, we can use a makeshift log csv to check if the DB was modified today.
	pd.DataFrame({'a':'this is only a log - check date on name'}, index=[0]).to_csv(params.db_data)
	print('>>>> Successfully saved on database!(3/3)')