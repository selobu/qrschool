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


class AsistenciaView(PermisionView):
    can_create = False
    can_edit = False
    can_delete = False
    page_size = 50  # the number of entries to display on the list view
    column_filters = ["id", "timestamp"]

    def get_pk_value(self, model):
        return f"{model.id}"


class MatriculaView(PermisionView):
    can_create = True
    can_edit = True
    can_delete = False
    page_size = 50  # the number of entries to display on the list view
    column_filters = ["anio", "periodo"]

    def get_pk_value(self, model):
        return f"{model.id}"


class GradoView(PermisionView):
    can_create = True
    can_edit = True
    can_delete = True
    page_size = 50  # the number of entries to display on the list view
    column_filters = ["id", "nombre"]
    column_details_exclude_list = (
        (
            [
                "estudiante",
            ],
        ),
    )
    form_columns = ["matricula", "nombre", "cupomaximo", "comentariomatricula"]

    def get_pk_value(self, model):
        return f"{model.id}"


def getviews() -> list:
    views = [
        UserView(Tb.User, app.Session()),  # type: ignore
        PerfilModuleview(Tb.PerfilModuloLnk, app.Session(), name="Permisos"),  # type: ignore
        AsistenciaView(Tb.Asistencia, app.Session(), name="Asistencia"),  # type: ignore
        MatriculaView(Tb.Matricula, app.Session(), name="Matricula"),  # type: ignore
        GradoView(Tb.Grado, app.Session(), name="Grado"),  # type: ignore
    ]
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

    def get_pk_value(self, model):
        return f"{model.id}"
