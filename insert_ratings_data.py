import os
import csv
from datetime import datetime
from app import db, UserRatings, app


def import_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        with app.app_context():
            for row in reader:
                print(row)
                rating_rounded = int(float(row['rating'])*2)
                rating = UserRatings(
                    user_id=int(row['userId']),
                    movie_id=int(row['movieId']),
                    rating=rating_rounded
                )
                db.session.add(rating)
                print('Rating added')
            db.session.commit()


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, 'app', 'data', 'ratings_small.csv')

    import_csv(csv_file_path)
    print("Data imported successfully!")
