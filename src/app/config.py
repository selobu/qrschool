# coding:utf-8
from os import environ
from pathlib import Path
from pydantic import BaseModel, SecretStr, EmailStr, HttpUrl
from pydantic import Field
from typing import Union

_rootpath = Path(__file__).parent.parent.parent.joinpath("secrets", "")


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


adminpassword = getData("db_root_password.txt", "MYSQL_ROOT_PASSWORD_FILE", "")

echo_value = environ.get("ECHO", False)
if isinstance(echo_value, str):
    if echo_value.lower() in ["true", "t"]:
        echo_value = True
    else:
        echo_value = False


class APIContact(BaseModel):
    name: str
    email: EmailStr
    url: HttpUrl
    telegram: HttpUrl


class Config(BaseModel):
    host: str
    port: Union[int, str, None] = Field(union_mode="left_to_right")
    db: str
    eng: str
    user: str = environ.get("MYSQL_USER", "adminuser")
    pwd: SecretStr = getData("db_password.txt", "MYSQL_PASSWORD_FILE", "")
    API_NAME: str = environ.get("APPNAME", "QRSchool api")
    VERSION: str = "0.0.2"
    API_URL_PREFIX: str = "/api"
    API_DESCRIPTION: str = "[source code](https://github.com/selobu/my_url)"
    admin_email: EmailStr = ""
    items_per_user: int = 50
    API_CONTACT: APIContact = APIContact(
        name="lteam",
        email="sebastian.lopez@gestionhseq.com",
        url="https://lteam.gestionhseq.com",
        telegram="https://t.me/selopez",
    )
    JWT_SECRET_KEY: SecretStr = getData("jwt_password.txt", "JWT_SECRET_KEY_FILE", "")
    WTF_CSRF_SECRET_KEY: SecretStr = (
        getData("jwt_password.txt", "JWT_SECRET_KEY_FILE", "") * 2
    )
    app: object = {}
    engine: object = {}
    ECHO: bool = echo_value  # type:ignore
    APP_NAME: str = environ.get("APPNAME", "QRSchool api")  # type:ignore
    FLASK_ADMIN_SWATCH: str = "cerulean"  # admin bootswatch theme
    ADMIN_TEMPLATE_NAME: str = "bootstrap4"
    TESTING: bool = False
    PER_PAGE: int = 50

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"{self.eng}://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.db}"


ProductionConfig = Config(
    eng="mysql+pymysql",
    host=environ.get("MYSQL_HOST", "localhost"),
    port=environ.get("MYSQL_PORT", "3306"),
    db=environ.get("MYSQL_DATABASE", "colegio2023"),
    ECHO=False,
)


DevelopmentConfig = Config(eng="sqlite", host="", port=None, db="tmp/foo.db", ECHO=True)


TestingConfig = Config(
    eng="sqlite", host="", port=None, db=":memory:", TESTING=True, ECHO=True
)


PythonAnywhereConfig = Config(
    eng="mysql+pymysql",
    port=None,
    user="selobu",
    host="selobu.mysql.pythonanywhere-services.com",
    db="selobu$colegio2023",
)
