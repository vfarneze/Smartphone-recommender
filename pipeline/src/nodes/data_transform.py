import logging
import pandas as pd
import os
import datetime


def done(client,params):
    '''Returns true there is data was treated today'''
    if (os.path.isfile(params.trans_data) and os.path.isfile(params.temp_data)):
        print('>>>> Already runned data_transform today... (2/3)')
        if params.force_execution:
            return False
        else:
            return True

    else:
        return False

def update(client,params):
    '''This function will clean columns from the obtained dataframe from jacotei.com.br.'''

    df = pd.read_csv(params.raw_data, encoding='cp1252')
    #treat columns 
    df.loc[:,'since'] = df.loc[:,'since'].apply(lambda x: x.split('desde')[1])

    # treating links:
    # 'https://www.jacotei.com.br' to jacotei links, by checking if starts with '/' (its the only one)

    df.loc[:,'piece_link'] = df.loc[:,'piece_link'].apply(lambda x: 'https://www.jacotei.com.br' + x if str(x).startswith('/') else x)

    # treating 'img', which will be the future 'destino_do_link' column
    # > drop '//img.i' from //img.ijacotei
    df.loc[:,'img'] = df.loc[:,'img'].apply(lambda x: 'jacotei.com.br' if x.startswith('//img.ijacotei') else x)
    
    # > drop 'https's from strings
    df.loc[:,'img'] = df.loc[:,'img'].apply(lambda x: x.split('/')[2] if x.startswith('http') else x)

    #rename columns:
    df.columns = ['modelo_celular', 'menor_preco', 'maior_preco', 'link_anuncio', 'data_anuncio', 'destino_do_link','timestamp']

    # reorder columns:
    df = df.loc[:,['modelo_celular', 'maior_preco','menor_preco', 'data_anuncio', 'destino_do_link', 'link_anuncio','timestamp']]

	# save to temporary file   
    df.to_csv(params.trans_data,sep=',',index=False, na_rep='NaN', encoding='cp1252')

    #minor modification for editing the timestamp that will be used to save the database
    df['timestamp'] = params.timestamp
    df.to_csv(params.temp_data,sep=',',index=False, na_rep='NaN', encoding='cp1252')

    print('>>>> Dataframe treated successfully! (2/3)')