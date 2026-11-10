from app.database import engine, Base
from app import models

# Create database tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")