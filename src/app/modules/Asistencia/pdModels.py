from app.apitools import createApiModelView
from flask_restx.fields import List, String, Integer, DateTime, Nested
from app.toolsapk import Tb
from dataclasses import dataclass

usr = createApiModelView(api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore


@dataclass
class QrRegisterList:
    qrs: List = List(
        String(description="User QR code", required=True),
        description="Listado de códigos Qr",
    )


@dataclass
class AsistenciaModel:
    id: Integer = (Integer(description="Asistencia id"),)
    total: Integer = (
        Integer(description="Cantidad total de personas en la asistencia"),
    )
    timestamp: DateTime = DateTime(description="Fecha de registro")


@dataclass
class Showuser:
    nombres: String = String(description="User name")
    apellidos: String = String(description="User surname")
    numeroidentificacion: String = String(description="Id number")
    grado: String = String(description="User's grade")


@dataclass
class ShowConsolidado:
    fecha: DateTime = DateTime(description="fecha")
    cantidad: Integer = Integer(description="Cantidad de ususarios")


@dataclass
class UsersResList:
    usrs: List = List(Nested(usr))
