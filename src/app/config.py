# coding:utf-8
from os import environ
from pathlib import Path
from pydantic import BaseModel, SecretStr, EmailStr, HttpUrl
from pydantic import Field, field_validator
from typing import Union
import re

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


# adminpassword = getData("db_root_password.txt", "MYSQL_ROOT_PASSWORD_FILE", "")

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
    host: str = Field(
        frozen=True, description="host", examples=["hocalhost", "127.0.0.1"]
    )
    port: Union[int, str, None] = Field(
        union_mode="left_to_right", frozen=True, examples=[8080, 8081]
    )
    dbport: Union[int, str, None] = Field(
        union_mode="left_to_right", frozen=True, examples=[3306]
    )
    db: str = Field(frozen=True)
    eng: str = Field(frozen=True)
    user: str = environ.get("MYSQL_USER", "adminuser")
    pwd: SecretStr = SecretStr(getData("db_password.txt", "MYSQL_PASSWORD_FILE", ""))
    API_NAME: str = environ.get("APPNAME", "QRSchool api")
    VERSION: str = Field(frozen=True, default="0.0.2")
    API_URL_PREFIX: str = Field(frozen=True, default="/api")
    API_DESCRIPTION: str = Field(frozen=True, default="")
    admin_email: EmailStr = Field(frozen=True, default="")
    items_per_user: int = Field(frozen=True, default=50)
    API_CONTACT: APIContact = Field(
        default=APIContact(
            name="lteam",
            email="sebastian.lopez@gestionhseq.com",
            url="https://lteam.gestionhseq.com",
            telegram="https://t.me/selopez",
        ),
        frozen=True,
    )
    JWT_SECRET_KEY: str = Field(
        default=getData("jwt_password.txt", "JWT_SECRET_KEY_FILE", ""),
        frozen=True,
    )
    # SecretStr = Field(
    #     default=SecretStr(getData("jwt_password.txt", "JWT_SECRET_KEY_FILE", "")),
    #     frozen=True,
    # )
    WTF_CSRF_SECRET_KEY: str = Field(
        default=getData("jwt_password.txt", "JWT_SECRET_KEY_FILE", "") * 2,
        frozen=True,
    )
    # SecretStr = Field(
    #     default=SecretStr(getData("jwt_password.txt", "JWT_SECRET_KEY_FILE", "") * 2),
    #     frozen=True,
    # )
    app: object = {}
    engine: object = {}
    SERVER_NAME: str | None = None
    ECHO: bool = Field(default=echo_value, frozen=True)  # type:ignore
    APP_NAME: str = Field(
        default=environ.get("APPNAME", "QRSchool api"), frozen=True
    )  # type:ignore
    FLASK_ADMIN_SWATCH: str = Field(
        default="cerulean", frozen=True
    )  # admin bootswatch theme
    ADMIN_TEMPLATE_NAME: str = Field(default="bootstrap4", frozen=True)
    TESTING: bool = Field(default=False, frozen=True)
    PER_PAGE: int = Field(default=50, frozen=True)

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        uri = f"{self.eng}://"
        if self.user not in (None, "None", ""):
            uri += f"{self.user}:{self.pwd.get_secret_value()}"
        if self.host not in (None, "None", ""):
            uri += f"@{self.host}"
        if self.port not in (None, "None", ""):
            uri += f":{self.dbport}"
        uri += f"/{self.db}"

        return uri

    @field_validator("host")
    @classmethod
    def validate_ip_regex(cls, ip_address: str) -> str:
        if ip_address == "":
            return ""
        compiled = re.compile(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$")
        if not compiled.match(ip_address):
            disallowed = re.compile(r"[^a-zA-Z\d\-]")
            if all(x and not disallowed.search(x) for x in ip_address.split(".")):
                return ip_address
            raise ValueError(f"The IP address {ip_address} is not valid")

        for ip_byte in ip_address.split("."):
            if int(ip_byte) < 0 or int(ip_byte) > 255:
                raise ValueError(f"The IP address {ip_address} is not valid")
        return ip_address


ProductionConfig = Config(
    eng="mysql+pymysql",
    host=environ.get("MYSQL_HOST", "127.0.0.1"),
    port=environ.get("PORT", "80"),
    dbport=environ.get("MYSQL_PORT", "3306"),
    db=environ.get("MYSQL_DATABASE", "colegio2023"),
    ECHO=False,
)


DevelopmentConfig = Config(
    eng="mysql+pymysql",
    host=environ.get("MYSQL_HOST", "127.0.0.1"),
    port=environ.get("PORT", "8081"),
    dbport=environ.get("MYSQL_PORT", "3306"),
    db=environ.get("MYSQL_DATABASE", "colegio2023"),
    ECHO=True,
)


TestingConfig = Config(
    user="",
    pwd="",
    eng="sqlite",
    host="",
    port="",
    dbport="",
    db=":memory:",
    TESTING=True,
    ECHO=True,
)


PythonAnywhereConfig = Config(
    eng="mysql+pymysql",
    port=None,
    dbport=None,
    user="selobu",
    host="selobu.mysql.pythonanywhere-services.com",
    db="selobu$colegio2023",
)
