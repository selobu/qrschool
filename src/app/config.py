# coding:utf-8

from os import environ
from pathlib import Path

adminuser = environ.get("MYSQL_ROOT_USER", "root")
user = environ.get("MYSQL_USER", "adminuser")

port = environ.get("MYSQL_PORT", "3306")
database = environ.get("MYSQL_DATABASE", "colegio2023")
host = environ.get("MYSQL_HOST", "localhost")
echo_value = environ.get("ECHO", False)
appname = environ.get("APPNAME")
_rootpath = Path(__file__).parent.parent.parent.joinpath("secrets", "")

# reading credentials
pth1 = _rootpath.joinpath("db_password.txt")
if not pth1.exists():
    userpassword = ""
    print("db_password not fount")
else:
    with open(
        environ.get("MYSQL_PASSWORD_FILE", _rootpath.joinpath("db_password.txt")), "r"
    ) as fopen:
        userpassword = fopen.readline()

pth2 = _rootpath.joinpath("db_root_password.txt")
if not pth1.exists():
    adminpassword = ""
    print("db_root_password not fount")
else:
    with open(
        environ.get(
            "MYSQL_ROOT_PASSWORD_FILE", _rootpath.joinpath("db_root_password.txt")
        ),
        "r",
    ) as fopen:
        adminpassword = fopen.readline()

pth3 = _rootpath.joinpath("db_root_password.txt")
if not pth1.exists():
    jwt_key = "1235sd35dsf4"
    print("jwt_key not fount")
else:
    with open(
        environ.get("JWT_SECRET_KEY_FILE", _rootpath.joinpath("jwt_password.txt")), "r"
    ) as fopen:
        jwt_key = fopen.readline()

if isinstance(echo_value, str):
    if echo_value.lower() in ["true", "t"]:
        echo_value = True
    else:
        echo_value = False


class Config(object):
    API_NAME: str = "QRSchool api"
    VERSION: str = "0.0.2"
    API_URL_PREFIX: str = "/api"
    API_DESCRIPTION: str = "[source code](https://github.com/selobu/my_url)"
    admin_email: str = ""
    items_per_user: int = 50
    API_CONTACT: object = {
        "name": "lteam",
        "email": "sebastian.lopez@gestionhseq.com",
        "url": "https://lteam.gestionhseq.com",
        "telegram": "https://t.me/selopez",
    }
    JWT_SECRET_KEY: str = jwt_key
    WTF_CSRF_SECRET_KEY: str = jwt_key * 2
    app: object = {}
    engine: object = {}
    ECHO: bool = echo_value  # type:ignore
    APP_NAME: str = appname  # type:ignore
    FLASK_ADMIN_SWATCH: str = "cerulean"  # admin bootswatch theme
    ADMIN_TEMPLATE_NAME: str = "bootstrap4"
    TESTING: bool = False
    PER_PAGE: int = 50


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{userpassword}@{host}:{port}/{database}"
    )


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/foo.db"


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
