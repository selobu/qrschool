__all__ = [
    "ns_asistencia",
    "qr_register_list",
    "usr",
    "usr_list_paginated",
    "asistencia",
]
from flask import current_app as app
from app.apitools import createApiModel
from flask_restx import fields
from app.toolsapk import Tb

api = app.api  # type: ignore

ns_asistencia = api.namespace(
    "asistencia", description="Registrar asistencia de usuarios"
)

usr = createApiModel(api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore

qr_register_list = api.model(
    "QrRegisterList",
    {
        "qrs": fields.List(
            fields.String(description="User QR code", required=True),
            description="Listado de códigos Qr",
        )
    },
)

usr_list_paginated = api.model(
    "UsersResList", {"usrs": fields.List(fields.Nested(usr))}
)
asistencia = api.model(
    "asistencia",
    {
        "asistenciaid": fields.Integer(description="Asistencia id"),
        "total": fields.Integer(
            description="Cantidad total de personas en la asistencia"
        ),
        "timestamp": fields.DateTime(description="Fecha de registro"),
    },
)
