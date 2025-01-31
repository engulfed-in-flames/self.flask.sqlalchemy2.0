from app import  db
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash

from . import bp
from .forms import LoginForm, SignupForm
from .models import Account


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = SignupForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            email = form.email.data
            hashed_password = generate_password_hash(form.password.data)

            account = Account(email=email, password=hashed_password)
            db.session.add(account)
            db.session.commit()
            login_user(account)
            return redirect(url_for("main.index"))
        except:
            db.session.rollback()
    return render_template("account/signup.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for("main.index"))
    return render_template("account/login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
