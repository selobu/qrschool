from flask import current_app as app
from flask_restx import Resource, fields
from sqlalchemy import select
from flask_jwt_extended import jwt_required

from app.apitools import createApiModel
from app.config import settings
from app.toolsapk import Tb, gethash, uuidgenerator

api = settings.app.api  # type: ignore
ns_usrs = api.namespace("usuario", description="Gestionar usuarios")

usr = createApiModel(api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore
usr_post = createApiModel(
    api,
    Tb.User,  # type: ignore
    "Usuario",
    readonlyfields=[
        "timestamp",
        "perfil_id",
        "grado_id",
        "grupoetnico_id",
        "is_active",
        "perfil_nombre",
    ],
    additionalfields={
        "password": fields.String(
            description="contraseña", required=True, min_length=9, default="***"
        )
    },
)

usr_register_list = api.model(
    "UsersResList", {"usrs": fields.List(fields.Nested(usr_post))}
)


@ns_usrs.route("/")
class UserList(Resource):
    """Listado de usuarios"""

    @ns_usrs.doc("Consulta la información de usuario")
    @ns_usrs.marshal_list_with(usr, code=200)
    @jwt_required()
    def get(self):
        """Retorna todos los usuarios

        límite actual 100 usuarios
        """
        with app.Session() as session:
            res = select(Tb.User).limit(100)
            users = session.execute(res).all()
        return [u[0] for u in users]

    @ns_usrs.doc("Registra un usuario")
    @ns_usrs.expect(usr_register_list)
    @ns_usrs.marshal_list_with(usr, code=201)
    def post(self):
        """Registra un usuario nuevo"""
        userlist = api.payload
        # Session.begin() set automatically the commit once it takes out the with statement
        res = list()
        with app.Session() as session:
            for user in userlist:
                res.append(Tb.User.register(**user))
            session.add_all(res)
            session.commit()
        with app.Session() as session:
            # Se generan los códigos qr de todos los usuarios agregados y se registra la contraseña
            qrs = list()
            passwords = list()
            for user in res:
                qrs.append(Tb.Qr.register(usuario_id=user.id, code=uuidgenerator()))
                passwords.append(
                    Tb.Auth.register(hash=gethash(user.password), usuario_id=user.id)
                )
            session.add_all(qrs)
            session.add_all(passwords)
            session.commit()
        return res


@ns_usrs.route("/<int:user_id>")
@ns_usrs.response(404, "User not found")
class User(Resource):
    """Usuario administracion"""

    @ns_usrs.doc("Información del usuario dado su id")
    @ns_usrs.marshal_with(usr)
    @jwt_required()
    def get(self, user_id):
        """Retorna la información del usuario"""
        with app.Session() as session:
            res = select(Tb.User).filter(Tb.User.id == user_id)
            user = session.execute(res).one()
        return user[0]

    @ns_usrs.doc("Actualiza la información del usuario")
    @ns_usrs.expect(usr)
    @ns_usrs.marshal_with(usr)
    @jwt_required()
    def put(self, user_id):
        """Actualiza la información de un usuario"""
        with app.Session() as session:
            # se actualiza la información de usuario
            user = Tb.User.register(id=user_id, **api.payload)
            session.add(user)
            session.commit()
        return user

    if False:

        @ns_usrs.doc("Elimina la información del usuario")
        @ns_usrs.response(204, "Ususario eliminado")
        def delete(self, user_id):
            """Elimina un usuario -- Acción irreversible"""
            with app.Session.begin() as session:
                res = select(Tb.User).filter_by(Tb.User.id == user_id)
                user = session.execute(res).one()
                session.delete(user)
            return 204
