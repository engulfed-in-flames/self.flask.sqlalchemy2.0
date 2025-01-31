from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo
from werkzeug.security import check_password_hash

from .models import Account


class SignupForm(FlaskForm):
    email = EmailField(
        label="Email",
        name="email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your email."},
    )
    password = PasswordField(
        label="Password",
        name="password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password."},
    )
    confirm = PasswordField(
        label="Confirm password",
        name="confirm-password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm your password."},
    )

    def validate(self, extra_validators=None):
        initial_validation = super(SignupForm, self).validate()
        if not initial_validation:
            return False

        account = Account.query.filter_by(email=self.email.data).first()
        if account:
            self.email.errors.append("The email already exists.")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match.")
            return False
        return True


class LoginForm(FlaskForm):
    email = StringField(
        label="Email",
        name="email",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your email."},
    )
    password = PasswordField(
        label="Password",
        name="password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password."},
    )

    def validate(self, extra_validators=None):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        account = Account.query.filter_by(email=self.email.data).first()
        if account and check_password_hash(account.password, self.password.data):
            login_user(account)
            return True
        else:
            self.password.errors.append("Email or password is invalid.")
            return False
