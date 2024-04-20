from flask import current_app as app
from sqlalchemy import select
from app.toolsapk import Tb


class QrListController:
    @staticmethod
    def get(parser):
        page = parser.get("page", default=1)
        per_page = parser.get("per_page", default=app.config["PER_PAGE"])
        with app.Session() as session:
            q = (
                select(Tb.Qr)
                .order_by(Tb.Qr.id.asc())
                .limit(per_page)
                .offset(per_page * (page - 1))
            )
            return session.scalars(q).all()

    @staticmethod
    def post(payload):
        qrlist = payload["qrs"]
        res = [""] * len(qrlist)
        with app.Session.begin() as session:
            for pos, qr in enumerate(qrlist):
                res[pos] = Tb.Qr.register(**qr)
            session.add_all(res)
            session.commit()
        return res


class UserGetQrController:
    @staticmethod
    def get(user_id):
        with app.Session() as session:
            # Se verifica que el usuario exista
            user = select(Tb.User).filter(Tb.User.id == user_id)
            usr = session.scalars(user).one()
            if usr.qr_id is None:
                # se genera un nuevo código QR
                qr = usr.generateqr()
                qr.usuario = usr
                session.add(qr)
                session.commit()
            return usr.qr_id.code


class QrController:
    @staticmethod
    def get(qr_id):
        with app.Session() as session:
            res = select(Tb.Qr).join(Tb.Qr.usuario).filter(Tb.Qr.code == qr_id)
            qr = session.scalars(res).one()
            return qr.usuario

    @staticmethod
    def put(qr_id, payload):
        with app.Session() as session:
            # se actualiza la información de usuario
            qr = Tb.Qr.register(id=qr_id, **payload)
            session.add(qr)
            session.commit()
        return qr
