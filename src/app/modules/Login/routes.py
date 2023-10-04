from flask import current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    jwt_required,
)
from flask_restx import Resource, fields
from sqlalchemy import select

from app.toolsapk import Tb, gethash

api = app.api  # type: ignore
ns_login = api.namespace("login", description="autenticacion")

auth = api.model(
    "Todo",
    {
        "email": fields.String(description="direccion de correo registrado"),
        "password": fields.String(description="Contraseña"),
    },
)

loginResponse = api.model(
    "LoginResponse",
    {
        "status": fields.String(description="estado de la autenticacion"),
        "auth": fields.Boolean(description="está autenticado?"),
        "fresh_access_token": fields.String(description="fresh access token"),
        "access_token": fields.String(description="Access token"),
        "email": fields.String(description="direccion de correo registrado"),
        "username": fields.String(description="Nombre del usario"),
        "qr": fields.String(description="Código QR del usuario"),
        "active": fields.Boolean(
            description="Indica si el usuario está activo en la plataforma"
        ),
        "modules": fields.List(fields.String(description="Modulo con permiso")),
    },
)


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
        usr = current_user
        if usr is None:
            return {
                "status": "not authenticated",
                "auth": False,
                "access_token": None,
                "user_id": None,
                "username": None,
                "lastname": None,
                "identi_ficacion": None,
            }, 400
        new_token = create_access_token(identity=usr, fresh=True)
        return {
            "status": "authenticated",
            "auth": True,
            "access_token": "Bearer " + new_token,
            "correo": usr.correo,
        }, 202

    @ns_login.doc("Lee el token")
    @ns_login.response(
        305, "Incorrect password or email, please check your credentials."
    )
    @ns_login.response(306, "email or password not found")
    @ns_login.expect(auth)
    @ns_login.marshal_with(loginResponse, code=200)
    def post(self):
        data = api.payload
        email = data["email"]
        passwordhash = gethash(data["password"])
        with app.Session() as session:
            # verifying credentials
            res = (
                select(Tb.Auth.hash, Tb.User)
                .join(Tb.Auth.usuario)
                .filter(Tb.User.correo == email)
            )
            readedhash, user = session.execute(res).all()[0]
            readmodules = False
            if user.perfil is not None:
                perfil = user.perfil_nombre.name
                readmodules = True
            else:
                modules = []

            userfullname = f"{user.nombres} {user.apellidos}"
            userqr = user.generateqr()
            active = user.is_active
            if readedhash is None:
                return "", 306
        if readmodules:
            with app.Session() as session:
                res = (
                    select(Tb.Module.modulename)
                    .join(Tb.PerfilModuloLnk.perfil)
                    .join(Tb.PerfilModuloLnk.modulo)
                    .filter(Tb.Perfil.nombreperfil == perfil)
                    .filter(Tb.PerfilModuloLnk.has_permision == True)  # noqa: E712
                )

                modules = session.scalars(res).all()

        if passwordhash == readedhash:
            access_token = create_access_token(identity=email, fresh=True)
            fresh_access_token = create_refresh_token(identity=email)
            return {
                "status": "authenticated",
                "auth": True,
                "active": active,
                "fresh_access_token": "Bearer " + fresh_access_token,
                "access_token": "Bearer " + access_token,
                "email": email,
                "username": userfullname,
                "qr": userqr,
                "modules": modules,
            }, 200
        return "", 305
