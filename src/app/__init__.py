# coding:utf-8
from os import getenv
import sys
from flask import Flask
from src.config import Settings, settings
from .toolsapk import Tb, db
from .imp_modules import modulesResolver
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager


def create_app(
    settings: Settings = settings,
):
    """Construct the core application."""
    app = Flask(__name__, static_folder="static", template_folder="templates")
    # making app globally available by calling settings
    settings.app = app
    setattr(app, "Tb", Tb)

    app.config["JWT_SECRET_KEY"] = settings.jwt_key

    with app.app_context():
        from . import modules
        from . import routes

        setattr(app, "api", modules.api)

        jwt = JWTManager(app)

        @jwt.user_identity_loader
        def user_identity_lookup(user):
            if isinstance(user, str):
                return user
            elif isinstance(user, Tb.User):
                return user.correo

        @jwt.user_lookup_loader
        def user_lookup_callback(_jwt_header, jwt_data):
            identity = jwt_data["sub"]
            with app.Session() as session:
                res = select(Tb.User).filter(Tb.User.correo == identity)
                return session.execute(res).one()[0]

        modules.init_app(app)

        # setting up additional routes
        routes.init_app(app)

        if "db" not in app.config:
            app.config["db"] = db
        if "tb" not in app.config:
            app.config["tb"] = Tb
        if "adminview" not in app.config:
            app.config["adminview"] = dict()

        modulesResolver(app)
        engine = settings.engine = create_engine(
            settings.database_uri, pool_recycle=3600, echo=True
        )

        setattr(app, "engine", engine)
        Session = sessionmaker(engine, expire_on_commit=False)
        setattr(app, "Session", Session)

        # @app.shell_context_processor
        def make_shell_context():
            return dict(db=db, Tb=Tb, Session=Session)

        app.shell_context_processor(make_shell_context)

        return app
