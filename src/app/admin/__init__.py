# coding:utf-8
from flask_admin import Admin
from .views import getviews


def init_app(app):
    admin = Admin(app, name=app.name, template_mode="bootstrap4")
    for view in getviews():
        admin.add_view(view)
