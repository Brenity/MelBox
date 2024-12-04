import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Change the database path if needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False
