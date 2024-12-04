from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config  # Import the Config class from config.py

# Initialize the database and login manager
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load configurations from the Config class
    app.config.from_object(Config)  # This line loads the configuration from config.py

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    from app.routes import bp  # Import routes blueprint from routes.py
    app.register_blueprint(bp)

    return app

# User loader function for Flask-Login
from app.models import User  # Import the User model

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Retrieve user by ID
