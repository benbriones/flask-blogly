"""Blogly application."""

import os

from flask import Flask, render_template, redirect, request
from models import db, connect_db, Post, User, DEFAULT_IMAGE_URL
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

""" USER routes"""


@app.get('/')
def home_page():
    """"index"""
    return redirect('/users')


@app.get('/users')
def show_user():
    """show users listings."""

    users = User.query.all()

    return render_template('users.html', users=users)


@app.get('/users/new')
def new_user_form():
    """form for new users"""

    return render_template('new_user_form.html')


@app.post('/users/new')
def create_user():
    """create a new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form.get('image_url') or None

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

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url', None)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()
    return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """deletes the user selected and any posts they have"""

    user = User.query.get_or_404(user_id)
    # posts = user.posts

    Post.query.filter(Post.user_id == user.id ).delete()
    # for post in posts:
    #     db.session.delete(post)

    db.session.delete(user)
    db.session.commit()
    # User.query.filter(User.id == user_id).delete()

    return redirect('/users')


""" POST routes"""


@app.get('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """displays the add post form """
    user = User.query.get_or_404(user_id)

    return render_template("new_post_form.html", user=user)


@app.post('/users/<int:user_id>/posts/new')
def process_add_post_form(user_id):
    """retrieves post form values, redirects to user details"""
    title = request.form.get('title')
    content = request.form.get('content')

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

# TODO: when passing named parameters, no space around '='


@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """shows a post, allows for editing and deleting a post"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)

    return render_template('post_detail.html', user=user, post=post)


@app.get('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """edit the current post"""

    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)


@app.post('/posts/<int:post_id>/edit')
def submit_edited_post(post_id):
    """submits edited post"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """deletes current post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    user_id = post.user_id

    return redirect(f'/users/{user_id}')
