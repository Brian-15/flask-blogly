"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag, PostTag
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

# Create

@app.route('/users/new', methods=['GET'])
def user_form():
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

@app.route('/tags/new', methods=['GET'])
def new_tag():
    """Display new tag form"""

    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    """handle new tag submission"""

    name = request.form["tag-name"]

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


# Read

@app.route('/', methods=['GET'])
def home():
    """Home page, redirect to /users"""

    return redirect('/users')

@app.route('/users', methods=['GET'])
def user_list():
    """Get list of all users"""
    
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/<int:id>', methods = ['GET'])
def user_profile(id):
    """Displays user profile"""

    user = User.query.get_or_404(id)
    posts = user.posts

    return render_template("profile.html", user=user, posts=posts)

@app.route('/posts/<int:id>', methods=['GET'])
def view_post(id):
    """Displays blog post details"""

    post = Post.query.get_or_404(id)

    return render_template('post.html', post=post)

@app.route('/tags', methods=['GET'])
def list_tags():
    """List all tags"""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:id>', methods=['GET'])
def show_tag(id):
    """Show tag details"""

    tag = Tag.query.get_or_404(id)

    return render_template('tag.html', tag=tag)


# Update

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

@app.route('/posts/<int:id>/edit', methods=['GET'])
def edit_post(id):
    """Show post edit form"""

    post = Post.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:id>/edit', methods=['POST'])
def submit_post_edit(id):
    """Updates post"""

    title = request.form["title"]
    content = request.form["content"]
    tag_ids = request.form.getlist("tags")

    edited_post = Post.query.get_or_404(id)
    edited_post.update(title, content)
    PostTag.update_tags(id, tag_ids)

    return redirect(f"/posts/{id}")

@app.route('/tags/<int:id>/edit', methods=['GET'])
def edit_tag(id):
    """Displays tag edit form"""

    tag = Tag.query.get_or_404(id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:id>/edit', methods=['POST'])
def submit_edit_tag(id):
    """Updates tag"""

    name = request.form["tag-name"]

    Tag.query.filter_by(id=id).update(dict(name=name))

    db.session.commit()

    return redirect('/tags')


# Delete

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """Removes user from database"""

    User.remove_user(id)

    return redirect('/users')

@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    """Removes post from database, redirects to post's author profile"""

    user_id = Post.remove_post(id)

    return redirect(f"/users/{user_id}")

@app.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    """Removes tag from database"""

    Tag.remove_tag(id)

    return redirect('/tags')


# Universal error route

@app.errorhandler(Exception)
def error_page(e):

    if isinstance(e, HTTPException):
        return render_template('error.html', error=e)

    return render_template('error.html', error=e), 500
