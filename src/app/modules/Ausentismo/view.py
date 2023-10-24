__all__ = [
    "ns_ausencia",
    "usr",
    "usr_list_paginated",
    "ausente",
    "showuser",
]
from flask import current_app as app
from app.apitools import createApiModel
from flask_restx import fields
from app.toolsapk import Tb

api = app.api  # type: ignore

ns_ausencia = api.namespace("ausencia", description="Registrar ausencia de usuarios")

usr = createApiModel(api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore

ausencia_register_list = api.model(
    "MissingRegisterList",
    {
        "ids": fields.List(
            fields.String(description="User id", required=True),
            description="Listado de identificación de usuarios",
        ),
        "Comentario": fields.String(description="Comentario ausencia", required=True),
        "fecha": fields.Date(description="Fecha de ausencia", required=True),
    },
)

usr_list_paginated = api.model(
    "UsersResList", {"usrs": fields.List(fields.Nested(usr))}
)
ausente = api.model(
    "ausente",
    {
        "ausenciaid": fields.Integer(description="ausencia id"),
        "fecha": fields.Date(description="Fecha ausencia reportada"),
        "timestamp": fields.DateTime(description="Fecha de registro en el sistema"),
        "nombres": fields.String(description="Nombres usuario ausente"),
        "apellidos": fields.String(description="Apellidos usuario ausente"),
        "numeroidentificacion": fields.String(
            description="Identificacion usuario ausente"
        ),
        "grado_id": fields.Integer(description="Identificacion del grado"),
        "activo": fields.Boolean(
            description="Indica si el ususario está activo en el sistema"
        ),
    },
)

showuser = api.model(
    "showuser",
    {
        "nombres": fields.String(description="User name"),
        "apellidos": fields.String(description="User surname"),
        "numeroidentificacion": fields.String(description="Id number"),
        "grado": fields.Integer(description="User's grade id"),
    },
)

showconsolidado = api.model(
    "showconsolidado",
    {
        "fecha": fields.DateTime(description="fecha"),
        "cantidad": fields.Integer(description="Cantidad de usuarios"),
    },
)
