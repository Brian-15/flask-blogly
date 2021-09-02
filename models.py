"""Models for Blogly."""

from enum import unique
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
    
    tags = db.relationship("Tag",
                           secondary="post_tag",
                           backref="posts")
    
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

class Tag(db.Model):
    """Tag model class"""

    __tablename__ = "tags"

    def __repr__(self):
        """Show tag representation"""

        t = self
        return f"<Tag {t.id} {t.name}>"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)
    

class PostTag(db.Model):
    """Model class for linking Tag and Post models"""

    __tablename__ = "post_tag"

    def __repr__(self):

        pt = self
        return f"<PostTag {pt.post_id} {pt.tag_id}>"
    
    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)

