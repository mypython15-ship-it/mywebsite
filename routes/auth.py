from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm
from extensions import db, login_manager
from models import User


auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            flash("Invalid username or password.")
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for("todolist.index"))
            else:
                flash("Invalid username or password.")

    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            flash("Email already used, please log in.")
            return redirect(url_for("auth.login"))

        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken, please choose another.")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(
            form.password.data,
            method='scrypt',
            salt_length=16
        )

        new_user = User(
            email=form.email.data,
            password=hashed_password,
            username=form.username.data
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))