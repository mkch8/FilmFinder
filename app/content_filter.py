from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from app import app
from app.models import UserRatings, Films


def get_user_liked_movies(user_id, min_rating=6):
    liked_movies = UserRatings.query.filter(UserRatings.user_id == user_id, UserRatings.rating >= min_rating).all()
    liked_movie_ids = [rating.movie_id for rating in liked_movies]
    return liked_movie_ids


def get_movie_recommendations(user_id, min_rating=6, num_recommendations=10):
    liked_movie_ids = get_user_liked_movies(user_id, min_rating)

    if not liked_movie_ids:
        return []

    # Get all movies
    movies = Films.query.all()
    movies_df = pd.DataFrame(
        [(movie.movie_id, movie.title, movie.genres, movie.keywords, movie.overview) for movie in movies],
        columns=['movie_id', 'title', 'genres', 'keywords', 'overview'])

    # Combine features into single string
    def combine_features(row):
        return f"{row['genres']} {row['keywords']} {row['overview']}"

    movies_df['combined_features'] = movies_df.apply(combine_features, axis=1)

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['combined_features'])

    # Compute cosine similarity matrix
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get indices of liked movies
    liked_indices = [movies_df[movies_df['movie_id'] == movie_id].index[0] for movie_id in liked_movie_ids]

    # Aggregate similarity scores
    similarity_scores = np.zeros(cosine_sim.shape[0])
    for idx in liked_indices:
        similarity_scores += cosine_sim[idx]

    # average similarity scores
    similarity_scores /= len(liked_indices)

    # Get movie indices sorted by similarity scores
    movie_indices = similarity_scores.argsort()[::-1]

    # Filter out already liked movies
    movie_indices = [i for i in movie_indices if movies_df['movie_id'].iloc[i] not in liked_movie_ids]

    # Get top N recommendations
    top_movie_indices = movie_indices[:num_recommendations]

    recommendations = movies_df.iloc[top_movie_indices]
    return recommendations['movie_id'].tolist()


# # Testing functionality
# with app.app_context():
#     print(get_movie_recommendations(1))

