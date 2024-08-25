from app import app, db

with app.app_context():
    db.drop_all()  # Drop all tables to ensure a fresh start
    db.create_all()  # Create all tables
    print("Database and tables created successfully!")
