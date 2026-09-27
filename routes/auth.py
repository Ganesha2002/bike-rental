from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("bikes.home"))

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            full_name=full_name,
            email=email,
            role="user"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("bikes.home"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):

            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("bikes.home"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("bikes.home"))