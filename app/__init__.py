from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the database and login manager
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Secret key and database URI
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a more secure key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database URI

    # Initialize the extensions (db and login_manager)
    db.init_app(app)
    login_manager.init_app(app)

    # Create the database tables (first time only)
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    # Import routes and register them
    from app.routes import bp  # Import blueprint from routes.py
    app.register_blueprint(bp)

    return app

# Define the user_loader function for Flask-Login
from app.models import User  # Import the User model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Retrieve the user from the database by their ID

