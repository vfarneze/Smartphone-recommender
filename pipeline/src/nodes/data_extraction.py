import logging
import datetime
import requests
import numpy as np
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import pandas as pd
import os

def get_redirection_link(link):
    return BeautifulSoup(requests.get(link).content,"lxml").find_all('a')[0]['href']


def done(client,params):
    '''Returns true there is data extracted today'''
    if os.path.isfile(params.raw_data):
        print('>>>> Already runned data_extraction today... (1/3)')
        if params.force_execution:
            return False
        else:
            return True

    else:
        return False

def update(client,params):
    '''This function gets all cellphones listed on https://www.jacotei.com.br.'''
    
    html_chunk_products = []

    for pag in np.arange(1, params.page_limit+1):
        
        params.page = pag
        print(f'loading page: {params.page} / with max of {params.number_per_page} phones per page')
        print(f'loading response for:' + params.url + f'{params.page}' + f'&n={params.number_per_page}')
        response = requests.get(params.url + f'{params.page}' + f'&n={params.number_per_page}')

        print(f'request status:{response.status_code}')

        if response.status_code != 200:
            print('response not [200]!!!')
            break
        
        else:
            print('loading soup...')
            soup = BeautifulSoup(response.content,'lxml')
            minisoup = soup.find_all('div', attrs={'id':'produtos'})[0]

            print('loading products...')
            #<article class="produtosS col-lg-4 col-md-4 col-sm-6 col-xs-12 produtos_vertical"> 
            html_chunk_products = html_chunk_products + minisoup.find_all('article', attrs={'class':'produtosS col-lg-4 col-md-4 col-sm-6 col-xs-12 produtos_vertical'})

    df = pd.DataFrame()

    for product_html in tqdm(html_chunk_products):
        # Getting product name
        name = product_html.find_all('h3', attrs={'class':"text-center hidden-sm hidden-lg hidden-md"})[0].find_all('a',attrs={'rel':"nofollow"})[0].text

        # getting link to product: <div class="carousel-inner" role="listbox">      
        link = product_html.find_all('a',attrs={'rel':"nofollow"})[0]['href']

        # "https://track2..." links redirect to other links. Getting them, instead of the original links.
        if link.startswith('https://track2'):
            link = get_redirection_link(link)

        #time since started in Jacotei
        since = product_html.find_all('p',attrs={'class':'text-center desde'})[0].text.strip()
        
        #Colecting information on image that sends user to origin page
        img = product_html.find_all('img')[0]['data-original']

        #getting prices.
        price_html_chunk = product_html.find_all('span', attrs={'class':"menorPrecoDestaque"})
        faixa_preco = price_html_chunk[0].text.strip('\n')

        #in case there is only one price
        if len(price_html_chunk) == 1:
            menorPrecoDestaque = faixa_preco

        #in case there are two prices: max and min.
        else:
            menorPrecoDestaque = price_html_chunk[1].text

        #updating dataframe (df)
        my_dict = {'nome': name,'faixa_preco':faixa_preco, 'menor_preco':menorPrecoDestaque,'piece_link': link,'since':since,'img':img}
        minidf = pd.DataFrame(my_dict,index=[0])
        df = pd.concat([df,minidf])

    # add column for time of extraction
    df['timestamp'] = datetime.datetime.now().ctime()

    df = df.reset_index(drop=True)
    df.to_csv(params.raw_data,sep=',',index=False, na_rep='NaN', encoding='cp1252')
    print('successfuly runned data_extraction today! (1/3)')