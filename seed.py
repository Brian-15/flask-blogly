"""Seed file - initialize data into database"""

from models.user import User, db
from models.post import Post
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

# Add a few sample blog posts
post1 = Post(title="SamplePost1", content="Hello World!", created_at="08/30/2021 07:37:16.00 PST", user_id=1)
post2 = Post(title="SamplePost2", content="Hellur World!", created_at="08/30/2021 07:37:16.00 PST", user_id=2)
post3 = Post(title="SamplePost3", content="Hello Wurld!", created_at="08/30/2021 07:37:16.00 PST", user_id=1)

# Add post data to staging area
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

# commit staged posts to database
db.session.commit()