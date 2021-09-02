"""Seed file - initialize data into database"""

from models import User, Post, Tag, PostTag, db
from app import app

# Initialize tables
db.drop_all()
db.create_all()

# Empty table if not empty
User.query.delete()

# Add a few sample users
user1 = User(first_name="John", last_name="Smith", image_url="https://images.unsplash.com/photo-1529665253569-6d01c0eaf7b6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1876&q=80")
user2 = User(first_name="Jane", last_name="Smith", image_url="https://images.unsplash.com/photo-1474552226712-ac0f0961a954?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=751&q=80")
user3 = User(first_name="Splenda", last_name="Bumblebatch", image_url="https://images.unsplash.com/photo-1579783483458-83d02161294e?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1928&q=80")

# Add user data to staging area
db.session.add_all([user1, user2, user3])

# commit staged users to database
db.session.commit()

# Add a few sample tags
tag1 = Tag(name="funny")
tag2 = Tag(name="happy")
tag3 = Tag(name="useful")

db.session.add_all([tag1, tag2, tag3])

db.session.commit()

# Add a few sample blog posts
post1 = Post(title="SamplePost1", content="Hello World!", created_at="08/30/2021 07:37:16.00 PST", user_id=1,
             tags=[tag1, tag2])
post2 = Post(title="SamplePost2", content="Hellur World!", created_at="08/30/2021 07:37:16.00 PST", user_id=2,
             tags=[tag2, tag3])
post3 = Post(title="SamplePost3", content="Hello Wurld!", created_at="08/30/2021 07:37:16.00 PST", user_id=1,
             tags=[tag1, tag3])

# Add post data to staging area
db.session.add_all([post1, post2, post3])

# commit staged posts to database
db.session.commit()
