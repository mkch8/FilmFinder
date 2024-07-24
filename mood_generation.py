from transformers import pipeline
from app import app, Films, db

emotion_classifier = pipeline('sentiment-analysis', model='j-hartmann/emotion-english-distilroberta-base')


# Analyze text for mood
def analyze_text(text):
    result = emotion_classifier(text)
    return result[0]['label'] if result else 'neutral'


# Get combined text for analysis
def get_combined_text(movie):
    combined_text = f"{movie.overview} {movie.genres} {movie.keywords}"
    return combined_text


# Update movie moods in database
def update_movie_moods():
    with app.app_context():
        movies = Films.query.all()
        count = 1
        for movie in movies:
            combined_text = get_combined_text(movie)
            mood = analyze_text(combined_text)
            movie.mood = mood
            db.session.add(movie)
            print(f'movie {count} added')
            count += 1
        db.session.commit()


if __name__ == '__main__':
    update_movie_moods()
    print("Movie moods updated successfully!")