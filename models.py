"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(),
                           nullable=False)

    last_name = db.Column(db.String(),
                          nullable=False)
    
    image_url = db.Column(db.String(),
                          nullable=False)

    posts = db.relationship('Post', backref='user')
    
    def __repr__(self):
        """Show info about user"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    def update(self, first_name, last_name, image_url):
        """Update user info with new values"""

        if (first_name):
            self.first_name = first_name

        if (last_name):
            self.last_name = last_name
        
        if (image_url):
            self.image_url = image_url

        db.session.add(self)
        db.session.commit()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """Post model class"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(),
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    def __repr__(self):
        """Show info about post"""

        p = self
        return f"<Post {p.id} {p.title} {p.created_at}>"
    
    def update(self, title, content):
        """Update user info with new values"""

        if (title):
            self.title = title
        
        if (content):
            self.content = content

        db.session.add(self)
        db.session.commit()