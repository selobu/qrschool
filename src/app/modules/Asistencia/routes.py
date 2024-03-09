from flask import current_app as app
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.apitools import ParserModel, changeoutputfmt
from app.toolsapk import Tb

from sqlalchemy import select, func, cast, Date, text

from .view import ns_asistencia, qr_register_list, asistencia, showuser, showconsolidado

parser = (
    ParserModel()
    .add_paginate_arguments()
    .add_outputfmt()
    .add_argument("id", type=str, help="name asistencia filter")
    .add_argument("timestamp", type=str, help="datetime")
)
api = app.api  # type: ignore


@ns_asistencia.route("/")
class AsistenciaList(Resource):
    """Listado de usuarios"""

    @changeoutputfmt(parser)
    @ns_asistencia.response(500, "Missing autorization header")
    @ns_asistencia.doc("Consulta el codigo qr de los usuarios")
    @ns_asistencia.marshal_list_with(asistencia, code=200)
    @ns_asistencia.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna los listados de asistencia paginados"""
        parser.parseargs()
        filters = {}
        for key, value in parser.args.items():
            if key == "format":
                continue
            if value is None:
                continue
            filters[key] = value

        page = [filters["page"], 1][filters["page"] is None]
        per_page = [filters["per_page"], app.config["PER_PAGE"]][
            filters["per_page"] is None
        ]
        filters.pop("page")
        filters.pop("per_page")

        with app.Session() as session:
            q = select(
                Tb.Asistencia.id,
                Tb.Asistencia.timestamp,
                func.count(Tb.Asistencia.id),
            ).join(Tb.Asistencia.userasistencia)
            for key, value in filters.items():
                q = q.filter(getattr(Tb.Asistencia, key).like(f"%{value.lower()}%"))
            q = (
                q.order_by(Tb.Asistencia.id.asc())
                .group_by(Tb.Asistencia.id)
                .limit(per_page)
                .offset(per_page * (page - 1))
            )
            result = [
                {"id": r[0], "total": r[2], "timestamp": r[1]}
                for r in session.execute(q).all()
            ]
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


@ns_asistencia.route("/<int:asistencia_id>/")
class Asistencia(Resource):
    """Listado de asistencia"""

    @changeoutputfmt(parser)
    @ns_asistencia.response(500, "Missing autorization header")
    @ns_asistencia.doc("Retorna el listado de asistentes paginados")
    @ns_asistencia.marshal_list_with(showuser, code=200)
    @ns_asistencia.expect(parser.paginate_model)
    @jwt_required()
    def get(self, asistencia_id):
        """Retorna los asistentes paginados"""
        page = parser.get("page", default=1)
        per_page = parser.get("per_page", default=app.config["PER_PAGE"])
        with app.Session() as session:
            q = (
                select(Tb.User)
                .join(Tb.User.asistencia)
                .filter(Tb.UsrAsistenciaLnk.asistencia_id == asistencia_id)
                .group_by(Tb.User.id)
                .limit(per_page)
                .offset(per_page * (page - 1))
            )

            def __getgrado(grado):
                try:
                    if grado is not None:
                        return grado.nombre
                except AttributeError:
                    return ""
                return ""

            result = [
                {
                    "nombres": r.nombres,
                    "apellidos": r.apellidos,
                    "numeroidentificacion": r.numeroidentificacion,
                    "grado": __getgrado(r.grado),
                }
                for r in session.scalars(q).all()
            ]
            return result


parseroutput = ParserModel().add_outputfmt()


@ns_asistencia.route("/last7/")
class AsistenciaLast7(Resource):
    """Listado de asistencia"""

    @changeoutputfmt(parser)
    @ns_asistencia.response(500, "Missing autorization header")
    @ns_asistencia.doc("Retorna asistencia de los ultimos 7 días")
    @ns_asistencia.marshal_list_with(showconsolidado, code=200)
    @ns_asistencia.expect(parseroutput.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna asistencia de los ultimos 7 días"""
        with app.Session() as session:
            q = (
                select(
                    cast(Tb.Asistencia.timestamp, Date).label("fecha"),
                    func.count().label("asistencia"),
                )
                .join(Tb.Asistencia.userasistencia)
                .group_by(cast(Tb.Asistencia.timestamp, Date))
                .order_by(text("fecha desc"))
                .limit(7)
            )
            result = [
                {"fecha": r[0], "cantidad": r[1]} for r in session.execute(q).all()
            ]
            return result
