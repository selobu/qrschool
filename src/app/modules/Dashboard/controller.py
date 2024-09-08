from flask import current_app as app
from sqlalchemy import select, func

# from typing import TYPE_CHECKING
from datetime import date
from pydantic import BaseModel

from app.modules.Asistencia.model import Asistencia, UsrAsistenciaLnk
from app.modules.Ausentismo.model import Ausentismo
from app.modules.Matriculas.model import Grado
from app.modules.User.model import User


class Output(BaseModel):
    Date: date
    Count: int


class Abscense(BaseModel):
    Date: date
    grade: str
    name: str
    last_name: str


class AttendanceByGrade(BaseModel):
    Date: date
    gradeid: int
    grade: str
    attendance: int


class DailyAttendanceController:
    @staticmethod
    def get(parser):
        with app.Session() as session:
            q = (
                select(
                    func.Date(Asistencia.timestamp),
                    func.count(UsrAsistenciaLnk.user_id),
                )
                .join(Asistencia, Asistencia.id == UsrAsistenciaLnk.asistencia_id)
                .group_by(func.Date(Asistencia.timestamp))
                .order_by(func.Date(Asistencia.timestamp).desc())
                .limit(7)
            )
            return [
                Output(Date=row[0], Count=row[1]) for row in session.execute(q).all()
            ]


class DailyAbscentController:
    @staticmethod
    def get(parser):
        with app.Session() as session:
            q = (
                select(func.Date(Ausentismo.timestamp), func.count(Ausentismo.id))
                .group_by(func.Date(Ausentismo.timestamp))
                .order_by(func.Date(Ausentismo.timestamp).desc())
                .limit(7)
            )
            return [
                Output(Date=row[0], Count=row[1]) for row in session.execute(q).all()
            ]


class TodayAbscentController:
    @staticmethod
    def get(parser):
        with app.Session() as session:
            q = (
                select(func.Date(Ausentismo.timestamp), Grado.nombre, Ausentismo)
                .join(User, User.id == Ausentismo.userausente_id)
                .join(Grado, Grado.id == User.grado_id)
                .limit(50)
            )
            res = []
            for row in session.execute(q).all():
                Date: date = row[0]
                Grade: str = row[1]
                rest: Ausentismo = row[2]
                res.append(
                    Abscense(
                        Date=Date,
                        grade=Grade,
                        name=rest.user_name,
                        last_name=rest.user_lastname,
                    )
                )
            return res


class AttendanceGroupPerDayController:
    @staticmethod
    def get(parser):
        with app.Session() as session:
            q = (
                select(
                    func.Date(Asistencia.timestamp),
                    Grado.id,
                    Grado.nombre,
                    func.count(UsrAsistenciaLnk.asistencia_id),
                )
                .join(Asistencia, Asistencia.id == UsrAsistenciaLnk.asistencia_id)
                .join(User, User.id == UsrAsistenciaLnk.user_id)
                .join(Grado, Grado.id == User.grado_id)
                .group_by(Asistencia.timestamp, Grado.id)
                .order_by(Asistencia.timestamp.desc())
                .limit(500)
            )
            res = []
            for row in session.execute(q).all():
                res.append(
                    AttendanceByGrade(
                        Date=row[0], gradeid=row[1], grade=row[2], attendance=row[3]
                    )
                )
            return res


# class UserListController:
#     def get(parser):
#         parser.parseargs()
#         page = parser.get("page", default=1)
#         per_page = parser.get("per_page", default=app.config["PER_PAGE"])
#         params = {
#             "nombres": parser.get("nombres", None),
#             "apellidos": parser.get("apellidos", None),
#             "grado_id": parser.get("grado_id", None),
#             "numeroidentificacion": parser.get("numeroidentificacion", None),
#         }
#         with app.Session() as session:
#             q = select(Tb.User)
#             for key, value in params.items():
#                 if value is None:
#                     continue
#                 tipe = parser[key].type
#                 if str(tipe) == str(str):
#                     q = q.filter(getattr(Tb.User, key).like(f"%{value.lower()}%"))
#                 elif str(tipe) == str(int):
#                     q = q.filter(getattr(Tb.User, key) == value)
#             q = (
#                 q.order_by(Tb.User.correo.asc())
#                 .limit(per_page)
#                 .offset(per_page * (page - 1))
#             )
#             return {"usrs": session.scalars(q).all()}

#     def post(payload):
#         userlist = payload
#         # Session.begin() set automatically the commit once it takes out the with statement
#         res = list()
#         try:
#             with app.Session() as session:
#                 for user in userlist:
#                     res.append(Tb.User.register(**user))
#                 session.add_all(res)
#                 session.commit()
#         except Exception as e:
#             raise BadRequest(f"Error adding the new user: {e.__cause__}")

#         with app.Session() as session:
#             # Se generan los códigos qr de todos los usuarios agregados y se registra la contraseña
#             qrs = list()
#             passwords = list()
#             for user in res:
#                 qrs.append(Tb.Qr.register(usuario_id=user.id, code=uuidgenerator()))
#                 passwords.append(
#                     Tb.Auth.register(hash=gethash(user.password), usuario_id=user.id)
#                 )
#             session.add_all(qrs)
#             session.add_all(passwords)
#             session.commit()
#         return res


# class UserController:
#     def get(user_id):
#         with app.Session() as session:
#             res = select(Tb.User).filter(Tb.User.id == user_id)
#             return session.scalars(res).one()

#     def put(user_id, payload):
#         with app.Session() as session:
#             # se actualiza la información de usuario
#             user = Tb.User.register(id=user_id, **payload)
#             session.add(user)
#             session.commit()
#         return user
