from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from .controller import LoginController
from .pdModels import Auth, LoginResponse

ns_login = app.api.namespace("login", description="autenticacion")

auth = Auth().get_model()
loginResponse = LoginResponse().get_model()


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@ns_login.route("/")
@ns_login.response(200, "success")
class Login(Resource):
    """Administracion de recursos"""

    @ns_login.response(500, "Missing autorization header")
    @ns_login.doc(description="Verifica si el usuario está autenticado")
    @jwt_required(refresh=True)
    def get(self):
        return LoginController.get()

    @ns_login.doc(description="Lee el token")
    @ns_login.response(
        305, "Incorrect password or email, please check your credentials."
    )
    @ns_login.response(306, "email or password not found")
    @ns_login.expect(auth)
    @ns_login.marshal_with(loginResponse, code=200)
    def post(self):
        return LoginController.post(app.api)
