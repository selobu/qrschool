# coding:utf-8
from flask_jwt_extended import JWTManager
from sqlalchemy import select


def init_app(app):
    Tb = app.Tb
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if isinstance(user, str):
            return user
        elif isinstance(user, Tb.User):
            return user.correo

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        with app.Session() as session:
            res = select(Tb.User).filter(Tb.User.correo == identity)
            return session.scalars(res).one()

    return jwt
