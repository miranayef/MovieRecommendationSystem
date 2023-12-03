import pickle
import streamlit as st
import requests
import pandas as pd

# Function to fetch movie poster using TMDB API
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies based on similarity
def recommend(movie, similarity_matrix, movie_data):
    index = movie_data[movie_data['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movie_data.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movie_data.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Streamlit App
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

# Load precomputed data
movies_content = pickle.load(open('artifacts/movie_list_content.pkl', 'rb'))
similarity_content = pickle.load(open('artifacts/similarity_content.pkl', 'rb'))
q_movies_demographic = pickle.load(open('artifacts/movie_demographic.pkl', 'rb'))

# Sidebar navigation
sidebar_choice = st.sidebar.radio("Navigation", ["Top Movies", "Movie Recommender"])
if sidebar_choice == "Top Movies":
    st.header('Top Movies Based on Demographic Filtering')

    # Display top movies based on demographic filtering with names and posters
    cols_top_movies = st.columns(5)
    for i, (title, poster_path) in enumerate(zip(q_movies_demographic.head(10)['title'], q_movies_demographic.head(10)['movie_id'])):
        with cols_top_movies[i % 5]:
            st.text(title)
            st.image(fetch_poster(poster_path))

else:
    # Header and dropdown for recommendation
    st.header('Movie Recommender System Using Machine Learning')
    movie_list = movies_content['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    # Button to trigger recommendation
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, similarity_content, movies_content)
        
        # Display recommendations in columns
        cols_recommendations = st.columns(5)
        
        for i in range(5):
            with cols_recommendations[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
