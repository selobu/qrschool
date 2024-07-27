from sqlalchemy import select, func
from flask import current_app as app
from datetime import date
from flask_jwt_extended import current_user
from app import Tb


class AusenciaController:
    @staticmethod
    def get(query_params):
        query_params.parseargs()
        filters = {}
        for key, value in query_params.args.items():
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
                tipe = query_params[key].type
                if str(tipe) == str(str):
                    q = q.filter(_getvalue(key).like(f"%{value.lower()}%"))
                elif str(tipe) == str(int):
                    q = q.filter(_getvalue(key) == value)
            # if (fecha := parser.get("fecha", None)) is not None:
            #    fecha = date.fromisoformat(fecha)
            #    q = q.filter(cast(Ausentismo.fecha, Date) == fecha)
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

    @staticmethod
    def post(api):
        useridlist = api.payload["ids"]
        comentario = api.payload["comentario"]
        fecha = date.fromisoformat(api.payload["fecha"])
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


class AusenciaLast7Controller:
    @staticmethod
    def get(query_args):
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
