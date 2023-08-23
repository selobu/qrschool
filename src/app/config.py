# coding:utf-8

from os import environ

from pydantic_settings import BaseSettings

adminpassword = environ.get("MYSQL_ROOT_PASSWORD")
adminuser = environ.get("MYSQL_ROOT_USER")
port = environ.get("MYSQL_PORT", "3306")
database = environ.get("MYSQL_DATABASE", "colegio2023")
host = environ.get("MYSQL_HOST", "localhost")
user = environ.get("MYSQL_USER", "root")
userpassword = environ.get("MYSQL_PASSWORD", "adminpassword123")
jwt_key = environ.get("JWT_SECRET_KEY", "superSecretpasswordneeds2BeChanged")


class Settings(BaseSettings):
    api_name: str = "Schoolar backend api"
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


settings = Settings()
