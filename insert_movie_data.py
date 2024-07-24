import os
import csv
from datetime import datetime
from app import db, Films, app


def import_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with app.app_context():
            for row in reader:
                print(row['id'])
                if row['release_date']:
                    try:
                        release_date = datetime.strptime(row['release_date'], '%Y-%m-%d').date()
                    except ValueError:
                        print(f"Skipping invalid date: {row['release_date']}")
                        continue

                movie = Films(
                    movie_id=int(row['id']),
                    title=row['title'],
                    vote_average=float(row['vote_average']),
                    vote_count=int(row['vote_count']),
                    status=row['status'],
                    release_date=release_date,
                    revenue=int(row['revenue']),
                    runtime=int(row['runtime']),
                    adult=row['adult'].lower() == 'true',
                    backdrop_path=row['backdrop_path'],
                    budget=int(row['budget']),
                    homepage=row['homepage'],
                    imdb_id=row['imdb_id'],
                    original_language=row['original_language'],
                    original_title=row['original_title'],
                    overview=row['overview'],
                    popularity=float(row['popularity']),
                    poster_path=row['poster_path'],
                    tagline=row['tagline'],
                    genres=row['genres'],
                    production_companies=row['production_companies'],
                    production_countries=row['production_countries'],
                    spoken_languages=row['spoken_languages'],
                    keywords=row['keywords'],
                    mood=None
                )
                db.session.add(movie)
                print('Movie added')
            db.session.commit()


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, 'app', 'data', 'TMDB_movie_dataset_v11_ratingsMT100.csv')

    import_csv(csv_file_path)
    print("Data imported successfully!")
