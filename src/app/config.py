# coding:utf-8

from os import environ
from typing import Union

from pydantic_settings import BaseSettings

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


class Settings(BaseSettings):
    api_name: str = "QRSchool api"
    version: str = "0.0.2"
    api_description: str = "[source code](https://github.com/selobu/my_url)"
    admin_email: str = ""
    items_per_user: int = 50
    database_test_uri: str = "sqlite:///database.db"
    api_contact: object = {
        "name": "lteam",
        "email": "sebastian.lopez@gestionhseq.com",
        "url": "https://lteam.gestionhseq.com",
        "telegram": "https://t.me/selopez",
    }
    database_uri: str = (
        f"mysql+pymysql://{user}:{userpassword}@{host}:{port}/{database}"
    )
    # database_uri: str = "sqlite:///database.db"
    jwt_key: str = jwt_key
    app: object = {}
    engine: object = {}
    echo: Union[str, bool] = echo_value
    appname: str = appname


settings = Settings()
