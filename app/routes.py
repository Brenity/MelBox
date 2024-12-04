from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User, Movie
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user
import os

# Define a Blueprint for routing
bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Static movie data (you can update this later with your own in-memory list)
MOVIES = [
    {"id": 1, "title": "Harry Potter and the Prisoner of Azkaban", "year": 1972, "genre": "Drama/Crime", "image_filename": "hp.jpg"},
    {"id": 2, "title": "Silence of the Lambs", "year": 2008, "genre": "Action/Thriller", "image_filename": "silence.jpg"},
    {"id": 3, "title": "Hellraiser", "year": 1994, "genre": "Crime/Drama", "image_filename": "hellraiser.jpeg"},
]


# Helper functions
def allowed_file(filename):
    """Check if a file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder):
    """Save an uploaded file to a specific folder and return the filename."""
    filename = secure_filename(file.filename)
    path = os.path.join('app/static', folder, filename)
    file.save(path)
    return filename



REVIEWS = {1: [], 2: [], 3: []}  # Mock reviews by movie ID

# Routes
@bp.route('/')
def home():
    featured_movies = MOVIES[:3]
    return render_template('index.html', movies=featured_movies)

@bp.route('/movies')
def movies():
    # Static list of movie objects with images
    return render_template('movie_list.html', movies=MOVIES)




@bp.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def movie(movie_id):
    # Find the movie by ID
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if not movie:
        flash('Movie not found!', 'danger')
        return redirect(url_for('main.home'))

    # Handle review submission (POST request)
    if request.method == 'POST':
        rating = request.form.get('rating')
        review_content = request.form.get('review')

        # Create a new review and store it
        new_review = {
            'rating': rating,
            'content': review_content,
            'user': current_user.username,
        }

        # Add the review to the REVIEWS dictionary
        if movie_id not in REVIEWS:
            REVIEWS[movie_id] = []
        REVIEWS[movie_id].append(new_review)

        # Store the recently rated movie in the current_user object
        current_user.recently_rated_movie = movie  # Storing the movie object
        
        flash('Your review has been added!', 'success')
        return redirect(url_for('main.movie', movie_id=movie_id))

    # Get the reviews for the movie

    reviews = REVIEWS.get(movie_id, [])
    
    return render_template('movie_page.html', movie=movie, reviews=reviews)

@bp.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    global MOVIES  # Declare MOVIES as a global variable
    # Find the movie by ID
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    
    if not movie:
        flash('Movie not found!', 'danger')
        return redirect(url_for('main.home'))

    # Remove the movie from the MOVIES list
    MOVIES = [m for m in MOVIES if m['id'] != movie_id]

    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('main.home'))



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('main.register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('main.register'))

        profile_picture = request.files.get('profile_picture')  # Fixed key
        if profile_picture and allowed_file(profile_picture.filename):
            filename = save_image(profile_picture, 'profile_pics')
        else:
            filename = 'default.jpg'

        new_user = User(username=username, email=email, profile_picture=filename)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('main.home'))

@bp.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_authenticated:
        flash('You must be signed in to add a movie.', 'warning')
        return redirect(url_for('auth.login')) 
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        year = request.form.get('year')
        genre = request.form.get('genre')

        if not title or not description:
            flash('Title and description are required!', 'danger')
            return redirect(url_for('main.add_movie'))

        movie_image = request.files.get('image')  # Fixed to 'image' as in the form
        if movie_image and allowed_file(movie_image.filename):
            filename = save_image(movie_image, 'images')
        else:
            filename = 'default.jpg'

        movie_id = len(MOVIES) + 1
        new_movie = {
            "id": movie_id, 
            "title": title, 
            "description": description, 
            "year": year, 
            "genre": genre, 
            "image_filename": filename
        }
        MOVIES.append(new_movie)

        flash('Movie has been added!', 'success')
        return redirect(url_for('main.movies'))

    return render_template('add_movie.html')



@bp.route('/rate_movie/<int:movie_id>', methods=['POST'])
@login_required
def rate_movie(movie_id):
    rating = request.form.get('rating')
    
    # Ensure the rating is a valid number (1-5)
    if rating not in ['1', '2', '3', '4', '5']:
        flash('Invalid rating! Please select a rating between 1 and 5.', 'danger')
        return redirect(url_for('main.movie', movie_id=movie_id))
    
    # Update the movie's rating
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if movie:
        movie['rating'] = float(rating)
    
    flash(f'You rated {movie["title"]} {rating} stars!', 'success')
    return redirect(url_for('main.profile'))


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@bp.route('/update_bio', methods=['POST'])
@login_required
def update_bio():
    bio = request.form.get('bio')
    if bio:
        current_user.bio = bio
        db.session.commit()
        flash('Your bio has been updated!', 'success')
    else:
        flash('Bio cannot be empty!', 'danger')

    return redirect(url_for('main.profile'))

@bp.route('/update_favorite_movie', methods=['POST'])
@login_required
def update_favorite_movie():
    favorite_movie = request.form.get('favorite_movie')
    
    # Update the user's favorite movie (store it in the session or any temporary storage)
    current_user.favorite_movie = favorite_movie

    # Optionally, save the favorite movie to a database if you later decide to use one
    db.session.commit()  # Commit if saving in DB

    flash("Favorite movie updated successfully!", "success")
    return redirect(url_for('main.profile'))

@bp.route('/update_profile_picture', methods=['GET', 'POST'])
@login_required
def update_profile_picture():
    if request.method == 'POST':
        # Check if a file was submitted
        profile_picture = request.files.get('profile_picture')
        if profile_picture and allowed_file(profile_picture.filename):
            # Save the new profile picture
            filename = save_image(profile_picture, 'profile_pics')
            
            # Update the current user's profile picture in the database
            current_user.profile_picture = filename
            db.session.commit()  # Commit the change
            
            flash('Your profile picture has been updated!', 'success')
        else:
            flash('Invalid file type! Please upload a valid image.', 'danger')
        
        return redirect(url_for('main.profile'))  # Redirect back to profile page
    
    return render_template('profile.html')  # In case of GET request

# This would go outside the Movie class, in a global context, such as your routes.py file
MOVIES = []  # List of all movies
movie_id_counter = 1  # Initial ID for the first movie

def add_movie(title, description, year, genre, image_filename):
    global movie_id_counter  # Access the global counter for auto-incrementing ids

    # Create a new Movie instance with the auto-incremented id
    new_movie = Movie(
        id=movie_id_counter,  # Automatically set the id
        title=title,
        description=description,
        year=year,
        genre=genre,
        image_filename=image_filename
    )
    
    MOVIES.append(new_movie)  # Add the new movie to the MOVIES list
    movie_id_counter += 1  # Increment the counter for the next movie

@bp.route('/movie/<int:movie_id>/add_review', methods=['POST'])
@login_required
def add_review(movie_id):
    movie = next((m for m in MOVIES if m['id'] == movie_id), None)
    if not movie:
        flash('Movie not found!', 'danger')
        return redirect(url_for('main.home'))

    # Get the review content from the form
    rating = request.form.get('rating')
    review_content = request.form.get('review')

    # Create a new review dictionary and store it
    new_review = {
        'rating': rating,
        'content': review_content,
        'user_id': current_user.id,  # Assuming you are using Flask-Login
    }
    
    # Add the review to the movie
    if movie_id not in REVIEWS:
        REVIEWS[movie_id] = []
    REVIEWS[movie_id].append(new_review)

    flash('Your review has been added!', 'success')
    return redirect(url_for('main.movie', movie_id=movie_id))  # Redirect back to the movie page
