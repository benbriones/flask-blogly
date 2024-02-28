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



connect_db(app)
db.create_all()


@app.get('/')
def home_page():
    return render_template('new_user_form.html')

# @app.get('/users')

# @app.get('/users/new')

# @app.post('/users/new')

# @app.get('/users/[user-id]')

# @app.get('/users/[user-id]/edit')

# @app.post('/users/[user-id]/edit')

# @app.post('/users/[user-id]/delete')




