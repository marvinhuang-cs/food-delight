import os
import config
from flask import Flask, render_template, session, g, flash, redirect, abort, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Favorite
from forms import SignupForm, LogInForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgres:///food_delight'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

toolbar = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"

API_KEY = config.API_KEY

###user sign up/log in/log out
@app.before_request
def add_user_to_g():
    """add current user to flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None
def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.context_processor
def api():
    return dict(API_KEY=API_KEY)

##routes
@app.route('/')
def main_page():
    if g.user:
        user = g.user

        recipes = Favorite.query.filter_by(user_id=user.id).all()
        return render_template("main.html", recipes=recipes)
    else:
        return render_template('main-anon.html')
    

        
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """create new user form and add to DB"""
    form = SignupForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            full_name=form.full_name.data
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("signup.html", form=form)

        do_login(user)
        return redirect("/")

    else:
        return render_template("signup.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():

    form = LogInForm()

    if form.validate_on_submit():
        user = User.login(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")

@app.route('/favorites')
def show_favorites():
    user = g.user

    recipes = Favorite.query.filter_by(user_id=user.id).all()

    return render_template("favorites.html", recipes=recipes)

@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    recipe_id=recipe_id

    return render_template("recipes.html", recipe_id=recipe_id)

@app.route('/recipes/<int:recipe_id>/fav', methods=['POST'])
def favorite_recipe(recipe_id):
    if not g.user:
        flash("Sign in to favorite.", "danger")
        return redirect("/")
    
    user = g.user
    id = recipe_id
    recipe_name = request.form.get('recipe_name')
    fav = Favorite(user_id=user.id, recipes=id, name=recipe_name)

    db.session.add(fav)
    db.session.commit()


    return redirect("/favorites")

@app.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_favorite(recipe_id):
    if not g.user:
        flash("Please sign in", "danger")
        return redirect("/")

    user = g.user
    recipe = Favorite.query.filter_by(recipes=recipe_id).first()
    if (recipe.user_id != user.id):
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(recipe)
    db.session.commit()

    return redirect("/favorites")

