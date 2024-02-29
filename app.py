"""Blogly application."""

import os

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
# debug = DebugToolbarExtension(app)

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


@app.get('/users/new')
def new_user_form():
    """form for new users"""

    return render_template('new_user_form.html')


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

    return redirect('/users')


@app.get('/users/<int:user_id>')
def users_post(user_id):
    """users personal listing"""

    user = User.query.get_or_404(user_id)

    return render_template('user_detail.html', user=user)


@app.get('/users/<int:user_id>/edit')
def edit_user(user_id):
    """edits current user page"""

    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


@app.post('/users/<int:user_id>/edit')
def process_edit(user_id):
    """Process edit form, redirect to users"""
    user = User.query.get_or_404(user_id)

    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    image_url = request.form.get('image_url', None)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()
    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """deletes the user selected"""

    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')
