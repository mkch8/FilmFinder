from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db
from app.forms import (LoginForm, RegistrationForm)
from app.models import User, UserRatings, Films
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
from app.content_filter import get_movie_recommendations
from app.svd_filter import get_recommendations, load_data, train_model
from uuid import uuid4
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
from email_validator import validate_email, EmailNotValidError
import csv


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return render_template('recommend.html')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # flash(f'Login for {form.username.data}', 'success')
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password_hash=generate_password_hash(form.password.data, salt_length=32))
        db.session.add(new_user)
        try:
            db.session.commit()
            flash(f'Registration for {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if User.query.filter_by(username=form.username.data):
                form.username.errors.append('This username is already taken. Please choose another')
            if User.query.filter_by(email=form.email.data):
                form.email.errors.append('This email address is already registered. Please choose another')
            flash(f'Registration failed', 'danger')
    return render_template('registration.html', title='Register', form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    if query:
        results = Films.query.filter(Films.title.ilike(f'%{query}%')).limit(5).all()
        results = [{"id": film.movie_id, "title": f"{film.title} ({film.release_date.strftime('%Y')})"} for film in results]
    else:
        results = []
    return jsonify(results)


@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    if request.method == 'POST':
        mood = request.form.get('mood')
        if mood == 'none':
            mood = None
        # get content based recommendations
        content_recommendations = get_movie_recommendations(current_user.user_id, 6, mood)
        print(content_recommendations)
        # get collaborative based recommendations
        ratings_df, films_df = load_data()
        svd_model = train_model(ratings_df)
        svd_recommendations = get_recommendations(current_user.user_id, svd_model, ratings_df, films_df, mood)
        print(svd_recommendations)
        # combine recommendations
        recommendations = content_recommendations + svd_recommendations
        films = Films.query.filter(Films.movie_id.in_(recommendations)).all()
        films_sorted = sorted(films, key=lambda x: recommendations.index(x.movie_id))
        return render_template('recommend.html', title='Recommend', films=films_sorted, mood=mood)


    return render_template('recommend.html', title='Recommend')


@app.route('/my_films', methods=['GET', 'POST'])
@login_required
def my_films():
    user_ratings = UserRatings.query.filter_by(user_id=current_user.user_id).all()
    film_ids = [rating.movie_id for rating in user_ratings]
    films = Films.query.filter(Films.movie_id.in_(film_ids)).all()

    ratings_dict = {rating.movie_id: rating.rating for rating in user_ratings}

    return render_template('my_films.html', films=films, ratings_dict=ratings_dict)


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/film/<int:film_id>', methods=['GET', 'POST'])
def film_page(film_id):
    film = Films.query.get_or_404(film_id)
    user_rating = None
    poster_path = 'https://image.tmdb.org/t/p/w500/' + film.poster_path

    if request.method == 'POST' and current_user.is_authenticated:
        rating = int(request.form['rating'])
        user_rating = UserRatings.query.filter_by(user_id=current_user.user_id, movie_id=film_id).first()
        if user_rating:
            user_rating.rating = rating
        else:
            user_rating = UserRatings(user_id=current_user.user_id, movie_id=film_id, rating=rating)
            db.session.add(user_rating)
        db.session.commit()
        return redirect(url_for('film_page', film_id=film_id))

    if current_user.is_authenticated:
        user_rating = UserRatings.query.filter_by(user_id=current_user.user_id, movie_id=film_id).first()

    return render_template('film_page.html', film=film, poster_path=poster_path,
                           user_rating=user_rating, user_logged_in=current_user.is_authenticated)


def is_valid_email(email):
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as error:
        return False
    return True


# Attempt to remove a file but silently cancel any exceptions if anything goes wrong
def silent_remove(filepath):
    try:
        os.remove(filepath)
    except:
        pass
    return


# Handler for 413 Error: "RequestEntityTooLarge". This error is caused by a file upload
# exceeding its permitted Capacity
# Note, you should add handlers for:
# 403 Forbidden
# 404 Not Found
# 500 Internal Server Error
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html'), 413
