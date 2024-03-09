from flask import current_app as app
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from app.apitools import ParserModel, changeoutputfmt
from app.toolsapk import Tb
from datetime import date
from sqlalchemy import select, func

from .view import (
    ns_ausencia,
    ausencia_register_list,
    ausente,
    showconsolidado,
)

parser = ParserModel()
user_paginate_model = (
    parser.add_paginate_arguments()
    .add_outputfmt()
    .add_argument("nombres", type=str, help="name as a filter")
    .add_argument("apellidos", type=str, help="surname as a filter")
    .add_argument("grado_id", type=int, help="grado_id as an integer")
    .add_argument("numeroidentificacion", type=str, help="id number as a filter")
    .add_argument("fecha", type=str, help="date formated as iso 8601")
    .paginate_model
)

api = app.api  # type: ignore


@ns_ausencia.route("/")
class ausenciaList(Resource):
    """Listado de usuarios"""

    @changeoutputfmt(parser)
    @ns_ausencia.response(500, "Missing autorization header")
    @ns_ausencia.doc("Retorna los listados de ausencia paginados")
    @ns_ausencia.marshal_list_with(ausente, code=200)
    @ns_ausencia.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna los listados de ausencia paginados"""
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

        def _getvalue(key):
            pairs = {
                "Ausentismo": [
                    "id",
                    "fecha",
                    "timestamp",
                ],
                "User": [
                    "nombres",
                    "apellidos",
                    "numeroidentificacion",
                    "grado_id",
                    "is_active",
                ],
            }
            if key in pairs["Ausentismo"]:
                return getattr(Tb.Ausentismo, key)
            else:
                return getattr(Tb.User, key)

        with app.Session() as session:
            q = select(
                Tb.Ausentismo.id,
                Tb.Ausentismo.fecha,
                Tb.Ausentismo.timestamp,
                Tb.User.nombres,
                Tb.User.apellidos,
                Tb.User.numeroidentificacion,
                Tb.User.grado_id,
                Tb.User.is_active,
            ).join(Tb.Ausentismo.userausente)
            for key, value in filters.items():
                tipe = parser[key].type
                if str(tipe) == str(str):
                    q = q.filter(_getvalue(key).like(f"%{value.lower()}%"))
                elif str(tipe) == str(int):
                    q = q.filter(_getvalue(key) == value)
            # if (fecha := parser.get("fecha", None)) is not None:
            #    fecha = date.fromisoformat(fecha)
            #    q = q.filter(cast(Tb.Ausentismo.fecha, Date) == fecha)
            q = q.limit(per_page).offset(per_page * (page - 1))
            keys = [
                "ausenciaid",
                "fecha",
                "timestamp",
                "nombres",
                "apellidos",
                "numeroidentificacion",
                "grado_id",
                "activo",
            ]
            result = [
                dict((key, value) for key, value in zip(keys, r))
                for r in session.execute(q).all()
            ]
            return result

    @ns_ausencia.doc("Registra ausencia de un usuario")
    @ns_ausencia.expect(ausencia_register_list)
    @ns_ausencia.response(200, "success")
    @jwt_required()
    def post(self):
        """Registra ausencia de un usuario"""
        useridlist = api.payload["ids"]
        comentario = api.payload["comentario"]
        fecha = date.fromisoformat(api.payload["fecha"])
        # Session.begin() set automatically the commit once it takes out the with statement
        with app.Session() as session:
            ausencias = []
            for userausente_id in useridlist:
                responsable = f"{current_user.nombres} {current_user.apellidos} - {current_user.correo} - {current_user.numeroidentificacion}"
                responsable = responsable[
                    : [len(responsable), 200][len(responsable) > 200]
                ]
                ausencias.append(
                    Tb.Ausentismo(
                        fecha=fecha,
                        userausente_id=userausente_id,
                        comentario=comentario,
                        responsableRegistro=responsable,
                    )
                )
            session.add_all(ausencias)
            session.commit()
        return [ausencia.id for ausencia in ausencias], 200


@ns_ausencia.route("/last7/")
class ausenciaLast7(Resource):
    """Listado de ausencia"""

    @ns_ausencia.response(500, "Missing autorization header")
    @ns_ausencia.doc("Retorna la ausencia de los ultimos 7 días")
    @ns_ausencia.marshal_list_with(showconsolidado, code=200)
    @jwt_required()
    def get(self):
        """Retorna ausencia de los ultimos 7 días"""
        with app.Session() as session:
            q = (
                select(
                    Tb.Ausentismo.fecha,
                    func.count(),
                )
                .join(Tb.Ausentismo.userausente)
                .group_by(Tb.Ausentismo.fecha)
                .order_by(Tb.Ausentismo.fecha.desc())
                .limit(7)
            )
            result = [
                {"fecha": r[0], "cantidad": r[1]} for r in session.execute(q).all()
            ]
            return result
