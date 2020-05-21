import streamlit as st
import pandas as pd

st.header('This is the title of my page.')

st.write('This is a plain text')

st.write('File changed.')

@st.cache
def load_dataset():
	return pd.DataFrame({'coluna1':[1,2,3,4],'coluna2':['pera', 'maçã', 'banana']})
	#return pd.read_csv('loan_dataset_train.csv')

df = load_dataset()

st.write(df.select_dtypes(exclude='object').fillna(0).style.highlight_max())

import seaborn as sns

sns.distplot(df.LoanAmount.fillna(0), hist=False)
st.pyplot()

st.code("""
pipeline = Pipeline(steps=[('preprocessing', StandardScaler()),
                           ('model', LogisticRegression())
                        ])
""", language='python')

st.sidebar.header('This is a plain text in the sidebar')

st.sidebar.checkbox('This is a checkbox', key='checkbox_2')
if st.checkbox('This is a checkbox'):
	st.write('Checkbox clicked!')
	sns.distplot(df.LoanAmount.fillna(0), hist=False)
	st.pyplot()

selected_button = st.radio('This is a radio button', ['optionA','optionB', 'optionC'])
st.write(selected_button)

if st.button('Hello'):
	st.balloons()
	st.write('__World__ :smile:')


from PIL import Image

uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file:
	image = Image.open(uploaded_file)
	st.image(image, caption='Uploaded Image.', use_column_width=True)