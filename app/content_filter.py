from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from app import app
from app.models import UserRatings, Films


def get_user_liked_movies(user_id, min_rating):
    liked_movies = UserRatings.query.filter(UserRatings.user_id == user_id, UserRatings.rating >= min_rating).all()
    liked_movie_ids = [rating.movie_id for rating in liked_movies]
    return liked_movie_ids


def get_movie_recommendations(user_id, min_rating, mood, num_recommendations=5,):
    liked_movie_ids = get_user_liked_movies(user_id, min_rating)

    if not liked_movie_ids:
        return []

    # Get all movies
    movies = Films.query.all()
    movies_df = pd.DataFrame(
        [(movie.movie_id, movie.title, movie.genres, movie.keywords, movie.overview, movie.mood) for movie in movies],
        columns=['movie_id', 'title', 'genres', 'keywords', 'overview', 'mood'])

    # combine features into single string, and add to our dataframe
    def combine_features(row):
        return f"{row['genres']} {row['keywords']} {row['overview']}"

    movies_df['combined_features'] = movies_df.apply(combine_features, axis=1)

    # vectorise the combined features
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['combined_features'])

    # cosine similarity matrix to compare movie vectors
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # get indices of liked movies
    liked_indices = [movies_df[movies_df['movie_id'] == movie_id].index[0] for movie_id in liked_movie_ids]

    # add similarity score together as we look at more than 1 film
    similarity_scores = np.zeros(cosine_sim.shape[0])
    for idx in liked_indices:
        similarity_scores += cosine_sim[idx]

    similarity_scores /= len(liked_indices)

    # sort movie indices by similarity score
    movie_indices = similarity_scores.argsort()[::-1]

    # filter out the liked movies (so we don't recommend movies already watched)
    movie_indices = [i for i in movie_indices if movies_df['movie_id'].iloc[i] not in liked_movie_ids]
    movie_indices = [i for i in movie_indices if movies_df['mood'].iloc[i] == mood]

    # get top n recommendations
    top_movie_indices = movie_indices[:num_recommendations]

    recommendations = movies_df.iloc[top_movie_indices]
    return recommendations['movie_id'].tolist()


# # Testing functionality
# with app.app_context():
#     print(get_movie_recommendations(1))

