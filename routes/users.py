from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

# from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from routes.database import db, User, MLModel


users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid credentials!", "danger")
    return render_template("login.html")


@users.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose another.", "error")
            return render_template("signup.html")

        user = User(username=username, role=role)
        user.set_password(password)

        try:
            # When you need to use the db:
            with current_app.app_context():
                # now you can use the db
                db.session.add(user)
                db.session.commit()
                flash("Signed up successfully!", "success")
                return redirect(url_for("users.login"))
        except IntegrityError:
            db.session.rollback()
            flash(
                "There was an error processing your signup. Please try again.", "error"
            )
            return render_template("signup.html")

    return render_template("signup.html")


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))
