# coding:utf-8
import jwt.exceptions
from flask import Blueprint
from flask_restx import Api

from app.config import settings

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
    }
}
app_blueprint = Blueprint(name="api", import_name="api", url_prefix="/api")

contact = settings.api_contact
if isinstance(contact, dict):
    name = contact["name"]
    contacturl = contact["url"]
    telegram = contact["telegram"]
doc = f"{settings.api_description}\n{name}\n{contacturl}\n{telegram}\n"
api = Api(
    app_blueprint,
    version=settings.version,
    title=settings.api_name,
    description=doc,
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


def init_app(app, csrf=None):
    if csrf is not None:
        csrf.exempt(app_blueprint)
    app.register_blueprint(app_blueprint)
