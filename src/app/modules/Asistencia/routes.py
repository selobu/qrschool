from flask import current_app as app
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required

from app.apitools import createApiModel
from app.toolsapk import Tb, gethash, uuidgenerator

api = app.api  # type: ignore

ns_asistencia = api.namespace(
    "asistencia", description="Registrar asistencia de usuarios"
)

usr = createApiModel(api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore

qr_register_list = api.model(
    "QrRegisterList",
    {
        "qrs": fields.List(
            fields.String(description="User QR code", required=True),
            description="Listado de códigos Qr",
        )
    },
)

usr_list_paginated = api.model(
    "UsersResList", {"usrs": fields.List(fields.Nested(usr))}
)


@ns_asistencia.route("/")
class AsistenciaList(Resource):
    """Listado de usuarios"""

    @ns_asistencia.doc("Registra un usuario")
    @ns_asistencia.expect(
        qr_register_list
    )  # @ns_asistencia.marshal_list_with(usr, code=201)
    @jwt_required()
    def post(self):
        """Registra listado de asistencia"""
        userlist = api.payload["qrs"]
        # Session.begin() set automatically the commit once it takes out the with statement
        res = list()
        with app.Session() as session:
            with session.begin():
                for user in userlist:
                    res.append(Tb.User.register(**user))
                session.add_all(res)
        with app.Session() as session:
            # Se generan los códigos qr de todos los usuarios agregados y se registra la contraseña
            qrs = list()
            passwords = list()
            with session.begin():
                for user in res:
                    qrs.append(Tb.Qr.register(usuario_id=user.id, code=uuidgenerator()))
                    passwords.append(
                        Tb.Auth.register(
                            hash=gethash(user.password), usuario_id=user.id
                        )
                    )
                session.add_all(qrs)
                session.add_all(passwords)
        return res
