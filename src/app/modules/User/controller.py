from flask import current_app as app
from sqlalchemy import select
from app.toolsapk import Tb, gethash, uuidgenerator
from werkzeug.exceptions import BadRequest


class UserListController:
    def get(parser):
        parser.parseargs()
        page = parser.get("page", default=1)
        per_page = parser.get("per_page", default=app.config["PER_PAGE"])
        params = {
            "nombres": parser.get("nombres", None),
            "apellidos": parser.get("apellidos", None),
            "grado_id": parser.get("grado_id", None),
            "numeroidentificacion": parser.get("numeroidentificacion", None),
        }
        with app.Session() as session:
            q = select(Tb.User)
            for key, value in params.items():
                if value is None:
                    continue
                tipe = parser[key].type
                if str(tipe) == str(str):
                    q = q.filter(getattr(Tb.User, key).like(f"%{value.lower()}%"))
                elif str(tipe) == str(int):
                    q = q.filter(getattr(Tb.User, key) == value)
            q = (
                q.order_by(Tb.User.correo.asc())
                .limit(per_page)
                .offset(per_page * (page - 1))
            )
            return {"usrs": session.scalars(q).all()}

    def post(payload):
        userlist = payload
        # Session.begin() set automatically the commit once it takes out the with statement
        res = list()
        try:
            with app.Session() as session:
                for user in userlist:
                    res.append(Tb.User.register(**user))
                session.add_all(res)
                session.commit()
        except Exception as e:
            raise BadRequest(f"Error adding the new user: {e.__cause__}")

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


class UserController:
    def get(user_id):
        with app.Session() as session:
            res = select(Tb.User).filter(Tb.User.id == user_id)
            return session.scalars(res).one()

    def put(user_id, payload):
        with app.Session() as session:
            # se actualiza la información de usuario
            user = Tb.User.register(id=user_id, **payload)
            session.add(user)
            session.commit()
        return user
