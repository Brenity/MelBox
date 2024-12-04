from app import create_app, db
# Importing the application factory and the database instance

app = create_app()
# Initializing the Flask application using the factory function

with app.app_context():
    # Activating the application context to access app-specific resources
    db.create_all()
    # Creating all database tables defined in the models
    print("Database tables created successfully.")
    # Confirmation message once tables are created
