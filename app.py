"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/', methods=['GET'])
def home():
    """Home page, redirect to /users"""

    return redirect('/users')

@app.route('/users', methods=['GET'])
def user_list():
    """Get list of all users"""
    
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new', methods=['GET'])
def show_user_form():
    """Show user form"""

    return render_template("new_user.html")

@app.route('/users/new', methods=['POST'])
def submit_user_form():
    """submit user form"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>', methods = ['GET'])
def get_user_profile(id):

    user = User.query.get_or_404(id)
    posts = user.posts

    return render_template("profile.html", user=user, posts=posts)

@app.route('/users/<int:id>/edit', methods = ['GET'])
def edit_user_form(id):
    """Show user edit form"""

    user = User.query.get_or_404(id)
    return render_template("edit_user.html", user=user)

@app.route('/users/<int:id>/edit', methods = ['POST'])
def submit_user_edit(id):
    """Update new user data"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]

    user = User.query.get_or_404(id)
    user.update(first_name, last_name, img_url)

    return redirect('/users')

@app.route('/users/<int:id>/delete', methods = ['POST'])
def delete_user(id):
    """Delete user from database"""

    Post.query.filter_by(user_id=id).delete()

    User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>/posts/new', methods=['GET'])
def post_form(id):
    """Show form to add a post for user whose id=id"""

    user = User.query.get_or_404(id)

    return render_template('new_post.html', user=user)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def post_form_submit(id):
    """Handle new post submission"""

    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{id}")

@app.route('/posts/<int:id>', methods=['GET'])
def view_post(id):
    """display blog post"""

    post = Post.query.get_or_404(id)

    return render_template('post.html', post=post)

@app.route('/posts/<int:id>/edit', methods=['GET'])
def edit_post(id):

    return render_template('edit_post.html', id=id)

@app.route('/posts/<int:id>/edit', methods=['POST'])
def submit_edit(id):

    title = request.form["title"]
    content = request.form["content"]

    edited_post = Post.query.get_or_404(id)
    edited_post.update(title, content)

    return redirect(f"/posts/{id}")

@app.route('/posts/<int:id>/delete')
def delete_post(id):

    post = Post.query.filter_by(id=id)
    user_id = Post.query.get_or_404(id).user_id

    post.delete()
    db.session.commit()

    return redirect(f"/users/{user_id}")


# Tag routes

@app.route('/tags', methods=['GET'])
def list_tags():
    """List all tags"""


    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:id>', methods=['GET'])
def show_tag(id):
    """Show tag details"""


    return render_template('tag.html', tag=tag)

@app.route('/tags/new', methods=['GET'])
def new_tag():
    """Display new tag form"""

    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    """handle new tag submission"""

    return redirect('/tags')

@app.route('/tags/<int:id>/edit', methods=['GET'])
def edit_tag(id):
    """display tag edit form"""

    return render_template('edit_tag.html', name=name)

@app.route('/tags/<int:id>/edit', methods=['POST'])
def submit_edit_tag(id):
    """handle edited tag submission"""

    return redirect('/tags')

@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    """delete tag"""

    redirect('/tags')

# Universal error route

@app.errorhandler(Exception)
def error_page(e):

    if isinstance(e, HTTPException):
        return render_template('error.html', error=e)

    return render_template('error.html', error=e), 500
