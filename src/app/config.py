# coding:utf-8

from os import environ
from pathlib import Path

adminuser = environ.get("MYSQL_ROOT_USER", "root")
user = environ.get("MYSQL_USER", "adminuser")

port = environ.get("MYSQL_PORT", "3306")
database = environ.get("MYSQL_DATABASE", "colegio2023")
host = environ.get("MYSQL_HOST", "localhost")
echo_value = environ.get("ECHO", False)
appname = environ.get("APPNAME", "QRSchool api")
_rootpath = Path(__file__).parent.parent.parent.joinpath("secrets", "")

userpythonanywhere = "selobu"
hostpythonanywhere = f"{userpythonanywhere}.mysql.pythonanywhere-services.com"
databasepythonanywhere = f"{userpythonanywhere}$colegio2023"


# reading credentials
def getData(filepath: str, key: str, default: str) -> str:
    pth = _rootpath.joinpath(filepath)
    if not pth.exists():
        filepath = str(environ.get(key))
    else:
        filepath = environ.get(key, str(pth))
    if Path(filepath).is_file():
        with open(filepath, "r") as fopen:
            return fopen.readline()
    return default


userpassword = getData("db_password.txt", "MYSQL_PASSWORD_FILE", "")
adminpassword = getData("db_root_password.txt", "MYSQL_ROOT_PASSWORD_FILE", "")
jwt_key = getData("jwt_password.txt", "JWT_SECRET_KEY_FILE", "")


if isinstance(echo_value, str):
    if echo_value.lower() in ["true", "t"]:
        echo_value = True
    else:
        echo_value = False


class Config(object):
    API_NAME: str = appname
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
    SQLALCHEMY_DATABASE_URI: str = ""


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{userpassword}@{host}:{port}/{database}"
    )
    ECHO = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/foo.db"
    ECHO = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    ECHO = True


class PythonAnywhereConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{userpythonanywhere}:{userpassword}@{hostpythonanywhere}/{databasepythonanywhere}"
