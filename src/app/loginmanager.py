# coding:utf-8
from flask_login import LoginManager
from sqlalchemy import select


def init_app(app):
    login_manager = LoginManager()
    login_manager.session_protection = "strong"

    Tb = app.Tb
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        with app.Session() as session:
            res = select(Tb.User).filter(Tb.User.id == user_id)
            try:
                return session.execute(res).one()[0]
            except Exception:
                return None

    return login_manager
