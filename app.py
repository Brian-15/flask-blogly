"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


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
    print(len(users))
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

    print(request.form)

    new_user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    print(new_user)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:id>', methods = ['GET'])
def get_user_profile(id):

    user = User.query.get_or_404(id)

    return render_template("profile.html", user=user)

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

    User.query.get_or_404(id).delete()
    db.session.commit()

    return redirect('/users')