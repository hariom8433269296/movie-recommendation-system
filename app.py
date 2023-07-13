import streamlit as st
import pickle
import pandas as pd
import requests
movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=1fb108e3ed460906c8032b5ad55e7600".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w780/"+data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    similar = similarity[movie_index]
    movies_list = sorted(list(enumerate(similar)),reverse = True,key = lambda x : x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movies.iloc[i[0]].id))
    return recommended_movies,recommended_movies_poster


st.title("Movie recommender system")
option = st.selectbox('which movies you want to get recommended by', movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(option)
    col = st.columns(5)
    for i in range(0,5):
        with col[i]:
            st.text(names[i])
            st.image(posters[i])



