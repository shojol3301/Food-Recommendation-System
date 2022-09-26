import difflib
from gettext import npgettext
import pickle
import streamlit as st
import pandas as pd
import pickle
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

food_dc = pickle.load(open('restaurant_data.pkl','rb'))
food = pd.DataFrame(food_dc)

loc_dc = pickle.load(open('restaurant_location.pkl','rb'))
loc = pd.DataFrame(loc_dc)

st.title('Food Recommender System')

selected_food = st.selectbox(
    'Select Your Favorite Item',
    food['items'].values)

selected_price = st.selectbox(
    'Select Your Price',
    food['price'].values)

selected_location = st.selectbox(
    'Select Your Location',
    loc['r_location'].values)


combined_features = food['r_name']+' '+food['price']+' '+food['package']
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)

find_close_match = difflib.get_close_matches(selected_food, food['items'].tolist())
close_match = find_close_match[0]
index_of_the_item = food[food['items'] == close_match]['index'].values[0]
similarity_score = list(enumerate(similarity[index_of_the_item]))
ssi = sorted(similarity_score, key = lambda x:x[1], reverse = True)

i = 1
for v in ssi:
  index = v[0]
  item_from_index = food[food.index==index]['items'].values[0]
    

if st.button('Recommend Other Items'):
    i = 1
    for v in ssi:
        index = v[0]
        item_from_index = food[food.index==index]['items'].values[0]
        if (i<6):
            st.write(item_from_index)
            i+=1