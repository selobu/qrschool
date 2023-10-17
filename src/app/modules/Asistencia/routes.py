from flask import current_app as app
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required

from app.apitools import createApiModel
from app.toolsapk import Tb

from sqlalchemy import select

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
asistencia = api.model(
    "asistencia",
    {
        "asistenciaid": fields.Integer(description="Asistencia id"),
        "total": fields.Integer(
            description="Cantidad total de personas en la asistencia"
        ),
        "timestamp": fields.DateTime(description="Fecha de registro"),
    },
)


@ns_asistencia.route("/")
class AsistenciaList(Resource):
    """Listado de usuarios"""

    @ns_asistencia.doc("Registra un usuario")
    @ns_asistencia.expect(qr_register_list)
    @ns_asistencia.marshal_with(asistencia, code=200)
    @jwt_required()
    def post(self):
        """Registra listado de asistencia"""
        qrlist = api.payload["qrs"]
        # Session.begin() set automatically the commit once it takes out the with statement
        with app.Session() as session:
            with session.begin():
                asistencia = Tb.Asistencia()
                session.add(asistencia)
            asistencia_id = asistencia.id

            with session.begin():
                q = (
                    select(Tb.User.id)
                    .join(Tb.Qr, Tb.Qr.usuario_id == Tb.User.qr_id)
                    .filter(Tb.Qr.code.in_(qrlist))
                )
                users = session.scalars(q).all()
                lnks = [
                    Tb.UsrAsistenciaLnk(asistencia_id=asistencia_id, user_id=userid)
                    for userid in users
                ]
                session.add_all(lnks)
        return {
            "asistenciaid": asistencia_id,
            "usuarios": len(users),
            "timestamp": asistencia.timestamp,
        }
