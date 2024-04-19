from app.apitools import createApiModelView, BaseMeta
from flask_restx.fields import List, String, Integer, DateTime, Nested, Date
from app.toolsapk import Tb
from dataclasses import dataclass
from flask import current_app as app

usr = createApiModelView(app.api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore


@dataclass
class QrRegisterList(BaseMeta):
    qrs: List = List(
        String(description="User QR code", required=True),
        description="Listado de códigos Qr",
    )


@dataclass
class AsistenciaModel(BaseMeta):
    id: Integer = Integer(description="Asistencia id")
    total: Integer = Integer(description="Cantidad total de personas en la asistencia")
    timestamp: DateTime = DateTime(description="Fecha de registro")


@dataclass
class Showuser(BaseMeta):
    nombres: String = String(description="User name")
    apellidos: String = String(description="User surname")
    numeroidentificacion: String = String(description="Id number")
    grado: String = String(description="User's grade")


@dataclass
class ShowConsolidado(BaseMeta):
    fecha: Date = Date(description="Fecha")
    cantidad: Integer = Integer(description="Cantidad de ususarios")


@dataclass
class UsersResList(BaseMeta):
    usrs: List = List(Nested(usr))
