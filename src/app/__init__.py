# coding:utf-8
from flask import Flask

from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config
from app.imp_modules import modulesResolver
from app.toolsapk import Tb, db

from app.shellcontex import cli
from flask_migrate import Migrate
from app import jwt, loginmanager

csrf = CSRFProtect()


def create_app(settings):
    """Contruct the core application."""
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # required by FLASK-WTFORMS
    app.secret_key = app.config["WTF_CSRF_SECRET_KEY"]

    with app.app_context():
        csrf.init_app(app)
        from . import modules, routes
        from . import admin
        from . import shellcontex

        api = modules.init_app(app, csrf=csrf)
        # setting up additional routes
        routes.init_app(app)

        engine = settings.engine = create_engine(
            settings.SQLALCHEMY_DATABASE_URI, pool_recycle=3600, echo=settings.echo
        )
        Session = sessionmaker(engine, expire_on_commit=False)

        items = {
            "db": db,
            "Tb": Tb,
            "adminview": dict(),
            "engine": engine,
            "Session": Session,
            "api": api,
        }

        for key, value in items.items():
            if not hasattr(app, key):
                setattr(app, key, value)

        modulesResolver(app)
        loginmanager.init_app(app)
        jwt.init_app(app)
        admin.init_app(app)
        shellcontex.init_app(app)
        cli.init_app(app)
        Migrate(app, db)
        Bootstrap(app)

        return app
