from . import db

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'director': self.director,
            'release_year': self.release_year,
            'genre': self.genre
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
