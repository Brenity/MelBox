class Config:
    # Secret key for sessions (ensure to change this in production)
    SECRET_KEY = 'your_secret_key_here'

    # Database configuration for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Use your database URI here (e.g., SQLite, PostgreSQL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable tracking modifications for performance
