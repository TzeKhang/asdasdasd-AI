import streamlit as st
import pandas as pd
from RevenueMovies import RevenueRecommender

# Load MovieLens data
movies = pd.read_csv("dataset/movies.csv")
ratings = pd.read_csv("dataset/ratings.csv")

# Initialize revenue recommender
revenue_recommender = RevenueRecommender("RevenueMovies.csv")

st.title("🎬 Movie Recommender System")

option = st.selectbox(
    "Choose a Recommendation Type",
    [
        "Top 5 Most-Selling Movies",
        "Top 5 Highest-Rated Movies",
        "Top 5 Movies by Genre",
        "Revenue-Based Recommendations"
    ]
)

if option == "Top 5 Most-Selling Movies":
    sales = ratings['movieId'].value_counts().reset_index()
    sales.columns = ['movieId', 'sales_count']
    top_sales = sales.merge(movies, on='movieId')
    st.subheader("Top 5 Most-Selling Movies")
    st.dataframe(top_sales[['title', 'sales_count']].head(5))

elif option == "Top 5 Highest-Rated Movies":
    avg_rating = ratings.groupby('movieId')['rating'].mean().reset_index()
    avg_rating.columns = ['movieId', 'avg_rating']
    top_rated = avg_rating.merge(movies, on='movieId')
    top_rated = top_rated.sort_values(by='avg_rating', ascending=False)
    st.subheader("Top 5 Highest-Rated Movies")
    st.dataframe(top_rated[['title', 'avg_rating']].head(5))

elif option == "Top 5 Movies by Genre":
    genre = st.text_input("Enter a genre (e.g., Action, Comedy, Drama):")
    if genre:
        genre_movies = movies[movies['genres'].str.contains(genre, case=False, na=False)]
        avg_rating = ratings.groupby('movieId')['rating'].mean().reset_index()
        genre_rated = genre_movies.merge(avg_rating, on='movieId')
        genre_rated = genre_rated.sort_values(by='rating', ascending=False)
        st.subheader(f"Top 5 {genre} Movies")
        st.dataframe(genre_rated[['title', 'genres', 'rating']].head(5))

elif option == "Revenue-Based Recommendations":
    st.subheader("💰 Revenue-Based Movie Recommender")

    # Let user pick a movie
    random_movies = revenue_recommender.get_random_movies(20)
    selected_movie = st.selectbox(
        "Pick a movie you watched:",
        random_movies['title'].values
    )

    if selected_movie:
        recs, selected_rev = revenue_recommender.recommend_by_revenue(selected_movie, tolerance=0.3, top_n=5)
        
        st.markdown(f"🎬 Since you watched **{selected_movie}** (Revenue: ${selected_rev:,}), you might also like:")
        if not recs.empty:
            st.dataframe(recs[['title', 'revenue']])
        else:
            st.info("⚠️ No similar revenue movies found.")
