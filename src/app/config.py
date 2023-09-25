# coding:utf-8

from os import environ
from typing import Union

adminpassword = environ.get("MYSQL_ROOT_PASSWORD")
adminuser = environ.get("MYSQL_ROOT_USER")
port = environ.get("MYSQL_PORT", "3306")
database = environ.get("MYSQL_DATABASE", "colegio2023")
host = environ.get("MYSQL_HOST", "localhost")
user = environ.get("MYSQL_USER", "root")
userpassword = environ.get("MYSQL_PASSWORD", "adminpassword123")
jwt_key = environ.get("JWT_SECRET_KEY", "superSecretpasswordneeds2BeChanged")
echo_value = environ.get("ECHO", False)
appname = environ.get("APPNAME", "QRSChool")
if isinstance(echo_value, str):
    if echo_value.lower() in ["true", "t"]:
        echo_value = True
    else:
        echo_value = False


class Config:
    API_NAME: str = "QRSchool api"
    VERSION: str = "0.0.2"
    API_URL_PREFIX: str = "/api"
    API_DESCRIPTION: str = "[source code](https://github.com/selobu/my_url)"
    admin_email: str = ""
    items_per_user: int = 50
    SQLALCHEMY_DATABASE_TEST_URI: str = "sqlite:///database.db"
    API_CONTACT: object = {
        "name": "lteam",
        "email": "sebastian.lopez@gestionhseq.com",
        "url": "https://lteam.gestionhseq.com",
        "telegram": "https://t.me/selopez",
    }
    SQLALCHEMY_DATABASE_URI: str = (
        f"mysql+pymysql://{user}:{userpassword}@{host}:{port}/{database}"
    )
    # SQLALCHEMY_DATABASE_URI: str = "sqlite:///database.db"
    JWT_SECRET_KEY: str = jwt_key
    WTF_CSRF_SECRET_KEY: str = jwt_key * 2
    app: object = {}
    engine: object = {}
    echo: Union[str, bool] = echo_value
    APP_NAME: str = appname
    FLASK_ADMIN_SWATCH: str = "cerulean"  # admin bootswatch theme
    ADMIN_TEMPLATE_NAME: str = "bootstrap4"
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = "mysql://user@localhost/foo"


class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:////tmp/foo.db"


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
