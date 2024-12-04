from werkzeug.security import generate_password_hash, check_password_hash
# Importing functions to hash and check passwords securely

from flask_sqlalchemy import SQLAlchemy
# Importing the SQLAlchemy ORM for database interactions

from flask_login import UserMixin
# Importing UserMixin to add user session management methods (like is_authenticated) to the User class

from app import db
# Importing the SQLAlchemy database instance from the app

# User model class to represent users in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Unique identifier for each user

    username = db.Column(db.String(150), unique=True, nullable=False)
    # Username field, must be unique and not null

    email = db.Column(db.String(150), unique=True, nullable=False)
    # Email field, must be unique and not null

    password = db.Column(db.String(60), nullable=False)
    # Password field, cannot be null, stored as a hashed string

    profile_picture = db.Column(db.String(150), nullable=True, default='default.jpg')
    # Profile picture filename field, defaults to 'default.jpg' if not set

    quote = db.Column(db.String(250), nullable=True)
    # User's personal quote, optional

    favorite_movie = db.Column(db.String(150), nullable=True)
    # User's favorite movie, optional

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    # Representation method to display user info

    def set_password(self, password):
        self.password = generate_password_hash(password)
    # Hashes the provided password and stores it in the database

    def check_password(self, password):
        return check_password_hash(self.password, password)
    # Checks if the provided password matches the hashed password in the database

# Movie class (not integrated with SQLAlchemy in this version)
class Movie:
    def __init__(self, id, title, description, year, genre, director=None, runtime=None, rating=None, language=None, release_date=None, image_filename=None):
        self.id = id  # Unique identifier for each movie
        self.title = title
        self.description = description
        self.year = year
        self.genre = genre
        self.director = director
        self.runtime = runtime
        self.rating = rating
        self.language = language
        self.release_date = release_date
        self.image_filename = image_filename
    # Constructor to initialize the movie object with various attributes

    def __repr__(self):
        return f"<Movie {self.title}>"
    # Representation method to display movie title

MOVIES = []
# A list to store movie objects (temporary storage for now)

movie_id_counter = 1  # Starting id value for the first movie
# A counter to assign unique ids to each movie in the MOVIES list
