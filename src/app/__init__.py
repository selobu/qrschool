# coding:utf-8
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import (
    Config,
    ProductionConfig,
    DevelopmentConfig,
    TestingConfig,
    PythonAnywhereConfig,
)
from app.imp_modules import modulesResolver
from app.toolsapk import Tb

from app.shellcontex import cli
from flask_migrate import Migrate
from app import jwt, loginmanager, shellcontex, admin, modules, routes
from app.toolsapk import Base
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from os import getenv

csrf = CSRFProtect()


def create_app(settings: Config | str = ProductionConfig):  # type: ignore
    """build the application core.

    settings: dict|str = 'local' | 'Python_anywhere' | 'dev' | 'test'

    """
    app = Flask(__name__, static_folder="static", template_folder="templates")

    if isinstance(settings, str):
        cfg = {
            "local": ProductionConfig,
            "Python_anywhere": PythonAnywhereConfig,
            "dev": DevelopmentConfig,
            "test": TestingConfig,
        }
        if settings == "":
            settings = getenv("FLASK_CONFIG", "local")
        elif settings not in cfg:
            raise KeyError(f"=> Unknown flask configuration! {settings}")
        settings: Config = cfg[settings]  # type: ignore

    app.config.from_object(settings)
    # required by FLASK-WTFORMS
    app.secret_key = app.config["WTF_CSRF_SECRET_KEY"]

    with app.app_context():
        csrf.init_app(app)
        api = modules.init_app(app, csrf=csrf)
        engine = create_engine(
            app.config["SQLALCHEMY_DATABASE_URI"],
            pool_recycle=3600,
            echo=app.config["ECHO"],
        )
        Session = scoped_session(
            sessionmaker(
                bind=engine, expire_on_commit=False, autocommit=False, autoflush=False
            )
        )

        items = {
            "Tb": Tb,
            "adminview": dict(),
            "engine": engine,
            "Session": Session,
            "api": api,
            "db": SQLAlchemy(app, model_class=Base),
        }
        db = items["db"]
        for key, value in items.items():
            if not hasattr(app, key):
                setattr(app, key, value)

        modulesResolver(app)
        routes.init_app(app)
        loginmanager.init_app(app)
        jwt.init_app(app)
        admin.init_app(app)
        shellcontex.init_app(app)
        cli.init_app(app)
        Migrate(app, db)
        Bootstrap(app)
        CORS(app, resources={r"/api/*": {"origins": "*"}})

        return app
