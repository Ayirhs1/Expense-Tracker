from app import app, db
from flask_migrate import Migrate

# Import all models for migrations
from models import Expense  

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    # Create all tables in the database
    db.create_all()
    
    # Run the Flask application
    app.run(port=5002)  # Change the port number as needed
