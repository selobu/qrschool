# coding:utf-8
from flask_admin import Admin
from .views import getviews, MyAdminIndexView
from app.config import settings


def init_app(app):
    admin = Admin(
        app,
        name=settings.appname,
        index_view=MyAdminIndexView(),
        template_mode="bootstrap4",
    )
    for view in getviews():
        admin.add_view(view)
