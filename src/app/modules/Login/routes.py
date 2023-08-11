from flask import current_app as app
from flask import request
from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, \
    jwt_required, current_user
from app.toolsapk import gethash
from flask_restx import Resource, fields
from src.config import settings
from app.toolsapk import Tb
from sqlalchemy import select

api = settings.app.api
ns_login = api.namespace("login", description="autenticacion")

auth = api.model(
    "Todo",
    {
        "email": fields.String(description="direccion de correo registrado"),
        "password": fields.String(description="Contraseña"),
    },
)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@ns_login.route("/")
@ns_login.response(200, "exitoso")
class Login(Resource):
    """Administracion de recursos"""
    @ns_login.response(500,"Missing autorization header")
    @ns_login.doc(description="Verifica si el usuario está autenticado")
    @jwt_required(refresh=True)
    def get(self):
        usr = current_user
        if usr is None:
            return {'status': 'not authenticated',
                    'auth': False,
                    'access_token': None,
                    'user_id': None,
                    'username': None,
                    'lastname': None,
                    'identi_ficacion': None}, 400
        new_token = create_access_token(
            identity=usr, fresh=True)
        return {'status': 'authenticated',
                'auth': True,
                'access_token': 'Bearer '+new_token,
                'correo': usr.correo}, 202
    
    @ns_login.doc("Lee el token")
    @ns_login.response(305, "Incorrect password or email, please check your credentials.")
    @ns_login.response(306, "email or password not found")
    @ns_login.expect(auth)
    def post(self):
        data = api.payload
        email = data["email"]
        passwordhash = gethash(data["password"])
        with app.Session() as session:
            # verifying credentials
            res = select(Tb.Auth.hash).\
                join(Tb.Auth.usuario).\
                filter(Tb.User.correo==email)
            readedhash = session.execute(res).scalar()
            if readedhash is None:
                return '', 306
        if passwordhash == readedhash:
            access_token = create_access_token(identity=email, fresh=True)
            fresh_access_token = create_refresh_token(identity=email)
            return {'status': "authenticated",
                'auth': True,
                'fresh_access_token': 'Bearer '+fresh_access_token,
                'access_token': 'Bearer '+access_token,
                'email': email,
                },  202
        return '', 305
