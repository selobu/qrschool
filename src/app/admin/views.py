__all__ = ["getviews"]

import flask_admin as admin
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from app.toolsapk import Tb
from flask import current_app as app, redirect, url_for, request
from flask_login import current_user


def modelview(model, **kwargs) -> ModelView:
    return ModelView(model, app.Session(), **kwargs)


def isactive():
    if current_user is None:
        return False
    return current_user.is_active


class PermisionView(ModelView):
    def is_accessible(self):
        if current_user is None:
            return False
        return current_user.is_active

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("login", next=request.url))


class PerfilModuleview(PermisionView):
    # form_base_class = SecureForm
    can_create = False
    can_edit = True
    can_delete = False
    page_size = 50  # the number of entries to display on the list view
    column_filters = ["perfil_id", "modulo_id"]
    column_editable_list = ["has_permision"]

    def get_pk_value(self, model):
        return f"{model.perfil_id.value},{model.modulo_id}"


class UserView(PermisionView):
    can_delete = False
    column_editable_list = ["is_active"]
    column_filters = ["nombres", "apellidos", "numeroidentificacion", "grado", "correo"]
    column_details_exclude_list = (
        [
            "id",
            "correo",
            "timestamp",
            "password_id",
            "calendario",
            "evaluacion",
            "qr_id",
            "ausente",
            "login",
        ],
    )
    form_columns = [
        "perfil",
        "grado",
        "grupoetnico",
        "is_active",
        "nombres",
        "apellidos",
        "numeroidentificacion",
        "fechaNacimiento",
        "rh",
        "telefonoContacto",
        "correo",
        "direccion",
        "telefono",
        "telefonoContacto",
    ]


def getviews() -> list:
    views = list()

    views.append(UserView(Tb.User, app.Session()))  # type: ignore
    views.append(PerfilModuleview(Tb.PerfilModuloLnk, app.Session(), name="Permisos"))  # type: ignore
    return views


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    @expose("/")
    def index(self):
        if not isactive():
            return redirect(url_for("login"))
        return super(MyAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        # login.logout_user()
        return redirect(url_for("index"))
