from sqlalchemy import select
from flask import current_app as app
from flask_jwt_extended import current_user, create_access_token, create_refresh_token
from app.toolsapk import Tb, gethash


class LoginController:
    @staticmethod
    def get():
        usr = current_user
        if usr is None:
            return {
                "status": "not authenticated",
                "auth": False,
                "access_token": None,
                "user_id": None,
                "username": None,
                "lastname": None,
                "identi_ficacion": None,
            }, 400
        new_token = create_access_token(identity=usr, fresh=True)
        return {
            "status": "authenticated",
            "auth": True,
            "access_token": "Bearer " + new_token,
            "correo": usr.correo,
        }, 202

    @staticmethod
    def post(api):
        data = api.payload
        email = data["email"]
        if email.endswith("\t"):
            email = email[:-1]
        passwordhash = gethash(data["password"])
        with app.Session() as session:
            # verifying credentials
            res = (
                select(Tb.Auth.hash, Tb.User)
                .join(Tb.Auth.usuario)
                .filter(Tb.User.correo == email)
            )
            result = session.execute(res).all()
            if len(result) == 0:
                return {
                    "status": "not authenticated",
                    "auth": False,
                    "active": False,
                    "fresh_access_token": "",
                    "access_token": "",
                    "email": email,
                    "username": "",
                    "qr": "",
                    "modules": [],
                }, 400
            readedhash, user = result[0]
            readmodules = False
            if user.perfil is not None:
                perfil = user.perfil_nombre.name
                readmodules = True
            else:
                modules = []

            userfullname = f"{user.nombres} {user.apellidos}"
            userqr = user.generateqr()
            photourl = user.photourl
            active = user.is_active
            if readedhash is None:
                return "", 306
        if readmodules:
            with app.Session() as session:
                res = (
                    select(Tb.Module.modulename)
                    .join(Tb.PerfilModuloLnk.perfil)
                    .join(Tb.PerfilModuloLnk.modulo)
                    .filter(Tb.Perfil.nombreperfil == perfil)
                    .filter(Tb.PerfilModuloLnk.has_permision == True)  # noqa: E712
                )

                modules = session.scalars(res).all()

        if passwordhash == readedhash:
            if isinstance(email, bytes):
                email = email.decode("utf-8")
            access_token = create_access_token(identity=email, fresh=True)
            fresh_access_token = create_refresh_token(identity=email)
            return {
                "status": "authenticated",
                "auth": True,
                "active": active,
                "fresh_access_token": "Bearer " + fresh_access_token,
                "access_token": "Bearer " + access_token,
                "email": email,
                "username": userfullname,
                "qr": userqr,
                "modules": modules,
                "photourl": photourl,
            }, 200
        return "", 305
