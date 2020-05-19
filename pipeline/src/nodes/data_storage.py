import logging
import pandas as pd
import sqlalchemy
import os


def done(client,params):
	'''Returns true there is data extracted today'''
	timestamp_column = pd.read_sql_query('SELECT DISTINCT timestamp FROM jacotei;', con=client.conn).loc[:,'timestamp'].unique()
	if params.timestamp in timestamp_column:
		print('>>>> Already runned data_stored today... (3/3)')
		if params.force_execution:
			return False
		else:
			return True

	else:
		return False

	
	

def update(client,params):
	'''	This function saves a stores the pipeline dataframe in a database.'''
	df = pd.read_csv(params.temp_data, encoding='cp1252')
	df.to_sql(params.table_name, client.conn, index=False, if_exists='append')
	print('>>>> Successfully saved on database!(3/3)')