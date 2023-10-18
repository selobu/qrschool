from flask import current_app as app
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required

from app.apitools import createApiModel, parser
from app.toolsapk import Tb

from sqlalchemy import select, func


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

    @ns_asistencia.response(500, "Missing autorization header")
    @ns_asistencia.doc("Consulta el codigo qr de los usuarios")
    @ns_asistencia.marshal_list_with(asistencia, code=200)
    @ns_asistencia.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna los listados de asistencia paginados"""
        page = parser.get("page", default=1)
        per_page = parser.get("per_page", default=app.config["PER_PAGE"])
        with app.Session() as session:
            q = (
                select(
                    Tb.Asistencia.id,
                    Tb.Asistencia.timestamp,
                    func.count(Tb.Asistencia.id),
                )
                .join(Tb.Asistencia.userasistencia)
                .order_by(Tb.Asistencia.timestamp.asc())
                .group_by(Tb.Asistencia.id)
                .limit(per_page)
                .offset(per_page * (page - 1))
            )
            print(q)
            result = [
                {"asistenciaid": r[0], "total": r[2], "timestamp": r[1]}
                for r in session.execute(q).all()
            ]
            print(f" => {result}")
            return result

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
