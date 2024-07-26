from sqlalchemy import select, func, cast, text, Date
from flask import current_app as app
from app import Tb

# Asistencia, UsrAsistenciaLnk
from app.modules.User.model import User
from app.modules.Qr.model import Qr


class AsistenciaListController:
    @staticmethod
    def get(parser):
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
        page = int(page)
        per_page = int(per_page)

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

    @staticmethod
    def post(api):
        qrlist = api.payload["qrs"]
        with app.Session() as session:
            with session.begin():
                asistencia = Tb.Asistencia()
                session.add(asistencia)
            asistencia_id = asistencia.id

            with session.begin():
                q = (
                    select(User.id)
                    .join(Qr, Qr.usuario_id == User.qr_id)
                    .filter(Qr.code.in_(qrlist))
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


class AsistenciaController:
    @staticmethod
    def get(parser, asistencia_id):
        page = parser.get("page", default=1)
        per_page = parser.get("per_page", default=app.config["PER_PAGE"])
        with app.Session() as session:
            q = (
                select(User)
                .join(User.asistencia)
                .filter(Tb.UsrAsistenciaLnk.asistencia_id == asistencia_id)
                .group_by(User.id)
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


class AsistenciaLast7Controller:
    @staticmethod
    def get():
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
