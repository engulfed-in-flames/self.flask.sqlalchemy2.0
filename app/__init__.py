import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


load_dotenv(".env.dev")

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_object=os.getenv("CONFIG_OBJECT")) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Crucial to avoid circular imports and to ensure that the app is properly configured
    # before any requests are made
    with app.app_context():
        register_extensions(app)
        register_blueprint(app)
        register_apis(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprint(app: Flask):
    from .blueprints.account import bp as account_bp

    app.register_blueprint(account_bp, url_prefix="/")

def register_apis(app: Flask):
    from .apis import api

    api.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from .blueprints.account.models import Account

    return Account.query.get(user_id)


@login_manager.unauthorized_handler
def handle_unauthorized():
    return redirect(url_for("main.index"))
