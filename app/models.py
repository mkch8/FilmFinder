from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Since we named our primary key "user_id", instead of "id", we have to override the
    # get_id() from the UserMixin to return the id, and it has to be returned as a string
    def get_id(self):
        return str(self.user_id)

    def __repr__(self):
        return f"user(id='{self.user_id}', '{self.username}', '{self.email}')"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class UsersFilms(db.Model):
    __tablename__ = 'users_films'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True, unique=True, nullable=False)
    movie_id = db.Column(db.String(20), db.ForeignKey('films.movie_id'), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f"user film(id='{self.user_id}', '{self.movie_id}')"


class Films(db.Model):
    __tablename__ = 'films'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    status = db.Column(db.String(50))
    release_date = db.Column(db.Date)
    revenue = db.Column(db.BigInteger)
    runtime = db.Column(db.Integer)
    adult = db.Column(db.Boolean)
    backdrop_path = db.Column(db.String(255))
    budget = db.Column(db.BigInteger)
    homepage = db.Column(db.String(255))
    imdb_id = db.Column(db.String(20))
    original_language = db.Column(db.String(10))
    original_title = db.Column(db.String(255))
    overview = db.Column(db.Text)
    popularity = db.Column(db.Float)
    poster_path = db.Column(db.String(255))
    tagline = db.Column(db.String(255))
    genres = db.Column(db.Text)
    production_companies = db.Column(db.Text)
    production_countries = db.Column(db.Text)
    spoken_languages = db.Column(db.Text)
    keywords = db.Column(db.Text)
    mood = db.Column(db.String(20))

    def __repr__(self):
        return f"user film(id='{self.movie_id}', title='{self.title}', release_date='{self.release_date}')"


class UserRatings(db.Model):
    __tablename__ = 'ratings'

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('films.movie_id'), primary_key=True)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return f"user rating(user_id={self.user_id}, movie_id={self.movie_id}, rating={self.rating}"

