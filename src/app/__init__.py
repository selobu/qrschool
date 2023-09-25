# coding:utf-8
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.config import Settings, settings
from app.imp_modules import modulesResolver
from app.toolsapk import Tb, db

from flask_login import LoginManager
from app.shellcontex import cli
from flask_migrate import Migrate

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.session_protection = "strong"

# adding shell commmands


def create_app(
    settings: Settings = settings,
):
    """Contruct the core application."""
    app = Flask(__name__, static_folder="static", template_folder="templates")
    # making app globally available by calling settings
    settings.app = app
    setattr(app, "Tb", Tb)
    app.config["JWT_SECRET_KEY"] = settings.jwt_key
    app.config["WTF_CSRF_SECRET_KEY"] = settings.jwt_key * 2
    app.secret_key = app.config["WTF_CSRF_SECRET_KEY"]
    # admin bootswatch theme
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

    with app.app_context():
        csrf.init_app(app)
        Bootstrap(app)
        from . import modules, routes
        from . import admin
        from . import shellcontex

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

        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            with app.Session() as session:
                res = select(Tb.User).filter(Tb.User.id == user_id)
                try:
                    return session.execute(res).one()[0]
                except Exception:
                    return None

        modules.init_app(app, csrf=csrf)

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
            settings.SQLALCHEMY_DATABASE_URI, pool_recycle=3600, echo=settings.echo
        )

        setattr(app, "engine", engine)
        Session = sessionmaker(engine, expire_on_commit=False)
        setattr(app, "Session", Session)

        admin.init_app(app)
        shellcontex.init_app(app)
        cli.init_app(app)

        app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
        print(settings.SQLALCHEMY_DATABASE_URI)
        Migrate(app, db)

        return app
