# coding:utf-8
import jwt.exceptions
from flask import Blueprint
from flask_restx import Api


def init_app(app, csrf=None):
    authorizations = {
        "apikey": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
        }
    }
    app_blueprint = Blueprint(
        name="api", import_name="api", url_prefix=app.config["API_URL_PREFIX"]
    )

    contact = app.config["API_CONTACT"]
    if isinstance(contact, dict):
        name = contact["name"]
        contacturl = contact["url"]
        telegram = contact["telegram"]
    doc = f"{app.config['API_DESCRIPTION']}\n{name}\n{contacturl}\n{telegram}\n"
    api = Api(
        app_blueprint,
        version=app.config["VERSION"],
        title=app.config["API_NAME"],
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

    if csrf is not None:
        csrf.exempt(app_blueprint)
    app.register_blueprint(app_blueprint)

    return api
