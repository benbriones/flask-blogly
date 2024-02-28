"""Blogly application."""

import os

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


@app.get('/')
def home_page():
    """"index"""
    return redirect('/users')


@app.get('/users')
def show_user():
    """show users listings."""

    data = User.query.all()

    return render_template('users.html', users=data)


# @app.get('/users/new')

@app.post('/users/new')
def create_user():
    """create a new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url', None)

    user = User(first_name=first_name,
                last_name=last_name,
                image_url=image_url)

    db.session.add(user)
    db.session.commit()

# @app.get('/users/[user-id]')

# @app.get('/users/[user-id]/edit')

# @app.post('/users/[user-id]/edit')

# @app.post('/users/[user-id]/delete')
