"""Seed file - initialize data into database"""

from models import User, db
from app import app

# Initialize tables
db.drop_all()
db.create_all()

# Empty table if not empty
User.query.delete()

# Add a few sample users

user1 = User(first_name="John", last_name="Smith")
user2 = User(first_name="Jane", last_name="Smith")
user3 = User(first_name="Splenda", last_name="Bumblebatch")

# Add user data to staging area
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# commit staged users to database
db.session.commit()