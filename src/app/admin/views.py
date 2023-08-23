__all__ = ["getviews"]
from flask_admin.contrib.sqla import ModelView
from app.toolsapk import Tb
from flask import current_app as app
from flask_login import current_user


def modelview(model, **kwargs) -> ModelView:
    return ModelView(model, app.Session(), **kwargs)


class PermisionView(ModelView):
    def is_accessible(self):
        if current_user is None:
            return False
        return current_user.is_active


class PerfilModuoleview(PermisionView):
    # form_base_class = SecureForm
    can_create = False
    can_edit = True
    can_delete = False
    page_size = 50  # the number of entries to display on the list view
    column_filters = ["perfil_id", "modulo_id"]
    column_editable_list = ["has_permision"]

    def get_pk_value(self, model):
        return f"{model.perfil_id.value},{model.modulo_id}"


def getviews() -> list:
    views = list()

    views.append(PermisionView(Tb.User, app.Session()))  # type: ignore
    views.append(PerfilModuoleview(Tb.PerfilModuloLnk, app.Session(), name="Permisos"))  # type: ignore
    return views
