# coding:utf-8
from flask import Blueprint, url_for
from flask_restx import Api, fields, Resource
from app.toolsapk import db, Tb as tb
import jwt.exceptions
from config import settings

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
    }
}
app_blueprint = Blueprint(name="api", import_name="api", url_prefix="/api")

api = Api(
    app_blueprint,
    version=settings.version,
    title=settings.api_name,
    description=f"{settings.api_description}\n"
    f"{settings.api_contact['name']}\n"
    f"{settings.api_contact['url']}\n"
    f"{settings.api_contact['telegram']}\n",
    authorizations=authorizations,
    security="apikey",
)


@api.errorhandler(jwt.exceptions.ExpiredSignatureError)
def handle_error(error):
    return {
        "code": "0001",
        "description": "Signanure expired",
        "message": str(error),
    }, 400


def init_app(app):
    app.register_blueprint(app_blueprint)