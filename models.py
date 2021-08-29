"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(),
                           nullable=False)

    last_name = db.Column(db.String(),
                          nullable=False)
    
    image_url = db.Column(db.String())
    
    def __repr__(self):
        """Show info about user"""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    def update(self, first_name, last_name, image_url):
        """Update user info with new values"""

        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

        db.session.add(self)
        db.session.commit()