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
from pathlib import Path

try:
    import sshtunnel

    TUNNELING_AVAILABLE = True
except Exception:
    TUNNELING_AVAILABLE = False

csrf = CSRFProtect()

runningLocal = getenv("RUNNING_LOCAL", False)
if runningLocal == "True":
    defaultConfig = ProductionConfig
else:
    defaultConfig = PythonAnywhereConfig


def create_app(settings: Config | str = defaultConfig):  # type: ignore
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
    if getenv("TUNNELING", False) in ("True", "true", True):
        if not TUNNELING_AVAILABLE:
            raise ValueError("Can't use tunneling please use\npoetry add sshtunnel")
        ssh_host = app.config["SSH_HOST"]
        ssh_port = app.config["SSH_PORT"]
        ssh_username = app.config["SSH_USER"]
        # ssh_pkey = config['db_qa01']['SSH_PKEY']
        sql_host = app.config["HOST"]
        sql_port = int(app.config["DBPORT"])
        public_key_path = str(
            Path(__file__).parent.parent.parent / "secrets/turingrsa.pub"
        )
        ssh_password_path = str(
            Path(__file__).parent.parent.parent / "secrets/pythonanywhere.txt"
        )
        with open(ssh_password_path, "r") as fopen:
            ssh_password = fopen.read().replace("\n", "")
        """
        https://help.pythonanywhere.com/pages/AccessingMySQLFromOutsidePythonAnywhere/
        Setting	        Value
        SSH Hostname:	your SSH hostname
        SSH Username:	your PythonAnywhere username
        SSH Password:	the password you use to log in to the PythonAnywhere website
        SSH Key file:	should not be necessary when you specify the password
        MySQL Hostname:	your PythonAnywhere database hostname, eg. yourusername.mysql.pythonanywhere-services.com
        MySQL Server Port:	3306
        Username:	your PythonAnywhere database username
        Password:	your PythonAnywhere database password
        Default Schema:	your database name, eg yourusername$mydatabase
        """
        sshtunnel.SSH_TIMEOUT = 5.0
        sshtunnel.TUNNEL_TIMEOUT = 5.0
        with sshtunnel.SSHTunnelForwarder(
            ssh_host=(ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            ssh_private_key=public_key_path,
            remote_bind_address=(sql_host, sql_port),
        ) as tunnel:
            app.config["PORT"] = tunnel.local_bind_port
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
                        bind=engine,
                        expire_on_commit=False,
                        autocommit=False,
                        autoflush=False,
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

    else:
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
                    bind=engine,
                    expire_on_commit=False,
                    autocommit=False,
                    autoflush=False,
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
