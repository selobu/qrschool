from app.apitools import createApiModelView, BaseMeta
from flask_restx.fields import String, List, Nested
from app.toolsapk import Tb
from dataclasses import dataclass


usr = createApiModelView("Usuario", Tb.User, readonlyfields=["active"])  # type: ignore
usr_post = createApiModelView(
    "Usuario",
    Tb.User,  # type: ignore
    readonlyfields=[
        "timestamp",
        "perfil_id",
        "grado_id",
        "grupoetnico_id",
        "is_active",
        "perfil_nombre",
    ],
    additionalfields={
        "password": String(
            description="contraseña", required=True, min_length=9, default="***"
        )
    },
)


@dataclass
class UsersResList(BaseMeta):
    usrs: List = List(Nested(usr_post))


@dataclass
class UsersResListPag(BaseMeta):
    usrs: List = List(Nested(usr))


usr_register_list = UsersResList().get_model()
usr_list_paginated = UsersResListPag().get_model()
