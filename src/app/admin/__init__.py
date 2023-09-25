# coding:utf-8
from flask_admin import Admin
from .views import getviews, MyAdminIndexView


def init_app(app):
    admin = Admin(
        app,
        name=app.config["APP_NAME"],
        index_view=MyAdminIndexView(),
        template_mode=app.config["ADMIN_TEMPLATE_NAME"],
    )
    for view in getviews():
        admin.add_view(view)
