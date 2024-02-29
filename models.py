"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

from sqlalchemy.sql import func

db = SQLAlchemy()

DEFAULT_IMAGE_URL = '/static/default_pic.jpg'

def connect_db(app):
    """Connect to database."""
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default = DEFAULT_IMAGE_URL
    )


class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default = func.current_timestamp(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    users = db.relationship('User', backref = 'posts')





