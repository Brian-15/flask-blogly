from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey
from models.user import db

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
    
    created_at = db.Column(db.DateTime,
                           nullable=False)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='posts')
    
    def __repr__(self):
        """Show info about post"""

        p = self
        return f"<Post {p.id} {p.title} {p.created_at}>"
    
    def update(self, title, content):
        """Update user info with new values"""

        self.title = title
        self.content = content

        db.session.add(self)
        db.session.commit()