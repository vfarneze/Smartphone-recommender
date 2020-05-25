import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import seaborn as sns
from nodes import recommender
from PIL import Image

def get_soup_from_url(url):
	"""This function gets an url and returns a bs4 soup"""

	headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
	}
	response = requests.get(url,headers=headers)
	soup = BeautifulSoup(response.content)
	return soup

st.header('What should be my next smartphone?')

st.write("""Dear user, welcome to the COQUI 0.1.0 interface!""")
st.write("""Its use is simple: you tell us how much you want to pay for your next smartphone and we simply recommend you one with the best cost-benefit!""")

st.sidebar.header('User interface')

#st.sidebar.checkbox("I accept the terms I didn't read!", key='checkbox_2')

user_input = st.sidebar.text_input("How much do you want to pay?", 'insert value here in R$, with no cents')
usr = ''

try:
	user_input = int(user_input)

except:
	pass

if type(user_input) != str:
	usr = int(user_input)


terms = st.sidebar.checkbox("I accept the terms I didn't read!", key='checkbox_2')

if type(usr) == int and st.sidebar.button('Show me my smartphone!') and terms:
	st.write('__Let us go!__ :smile:')	

	#--------------------------------------------------------------------------------------------------#
	# Create a text element and let the reader know the data is loading.
	data_load_state = st.text('Loading data...')
	# Load 10,000 rows of data into the dataframe.
	results = pd.read_csv('../websites-to-scrapp/kmeans_results.csv', index_col='Unnamed: 0')
	# Notify the reader that the data was successfully loaded.
	data_load_state.text('Loading data...done!')


	answer = recommender.get_my_smartphone(dataset=results, money=usr, upper=1.2)

	winner_url = answer[0]
	winner_price = answer[1]
	suggestion_url = answer[2]
	suggestion_price  = answer[3]

	soup = get_soup_from_url(winner_url)

	try: 
		try:
			name = soup.find_all('img', attrs={'class': "principal center-block"})[0]['alt']
		except:
			name = soup.find_all('div', attrs={'class':"image_prod"})[0].find_all('img')[0]['alt']

		try:
			img_url = soup.find_all('img', attrs={'class': "principal center-block"})[0]['data-zoom-image']
		except:
			img_url = soup.find_all('div', attrs={'class':"image_prod"})[0].find_all('img')[0]['data-original']

		response = requests.get(img_url)

		file = open("imagem_celular.png", "wb")
		file.write(response.content)
		file.close()

		image = Image.open('imagem_celular.png')
		st.image(image, caption='Uploaded Image.', use_column_width=True)
		#imgplot = plt.imshow(image)
		#plt.axis('off')
		#plt.grid(b=None)
		#plt.show()
		#st.pyplot()
		#st.image(image)

		st.write('Sua sugestão é:\n')
		st.write(name)
		st.write(f'\nMelhor custo/benefício: R${winner_price},00.')
		st.write('\nEncontre em:\n')
		st.write(winner_url)

	except:
		st.write('Produto recomendado não disponível!')