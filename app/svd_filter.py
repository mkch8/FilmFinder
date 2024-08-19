import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from app.models import UserRatings, Films  # Import your models
from app import app


# load films and rating data from the database
def load_data():
    ratings = UserRatings.query.all()
    ratings_df = pd.DataFrame([(r.user_id, r.movie_id, r.rating) for r in ratings],
                              columns=['user_id', 'movie_id', 'rating'])

    films = Films.query.all()
    films_df = pd.DataFrame([(f.movie_id, f.title, f.mood) for f in films],
                            columns=['movie_id', 'title', 'mood'])

    return ratings_df, films_df


# train the SVD model using data pulled from 'UserRatings'
def train_model(ratings_df):
    # convert to readable format and normalise
    reader = Reader(rating_scale=(ratings_df['rating'].min(), ratings_df['rating'].max()))
    data = Dataset.load_from_df(ratings_df[['user_id', 'movie_id', 'rating']], reader)

    trainset, testset = train_test_split(data, test_size=0.1)
    svd = SVD()
    svd.fit(trainset)

    return svd


# Generate recommendations for a specific user with a mood filter
def get_recommendations(user_id, svd, ratings_df, films_df, mood, n_recommendations=5):
    # Filter the films based on the selected mood
    if mood:
        mood_filtered_films = films_df[films_df['mood'] == mood]
        filtered_movie_ids = mood_filtered_films['movie_id'].tolist()
    else:
        filtered_movie_ids = films_df['movie_id'].tolist()

    # Get the movies the user has already rated
    user_rated_movies = ratings_df[ratings_df['user_id'] == user_id]['movie_id'].tolist()

    # Identify the unseen movies with the selected mood
    unseen_movies = set(filtered_movie_ids) - set(user_rated_movies)

    # Predict ratings for all unseen movies
    predictions = []
    for movie_id in unseen_movies:
        pred = svd.predict(user_id, movie_id)
        predictions.append((movie_id, pred.est))

    # Sort predictions by estimated rating in descending order
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Get top N recommendations
    top_n_recommendations = predictions[:n_recommendations]

    # Get the recommended movies' details
    recommended_movie_ids = [movie_id for movie_id, _ in top_n_recommendations]
    recommended_movies = films_df[films_df['movie_id'].isin(recommended_movie_ids)]

    return recommended_movies['movie_id'].tolist()


# Test script
if __name__ == "__main__":
    with app.app_context():
        ratings_df, films_df = load_data()
        svd_model = train_model(ratings_df)
        user_id = 1
        selected_mood = 'joy'
        recommendations = get_recommendations(user_id, svd_model, ratings_df, films_df, selected_mood)
        print(recommendations)

