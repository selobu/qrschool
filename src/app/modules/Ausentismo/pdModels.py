from flask_restx.fields import List, String, Date, Integer, DateTime, Boolean, Nested
from dataclasses import dataclass
from app.apitools import createApiModelView
from app.toolsapk import Tb
from flask import current_app as app

usr = createApiModelView(app.api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore


@dataclass
class MissingRegisterList:
    ids: List = List(
        String(description="User id", required=True),
        description="Listado de identificación de usuarios",
    )
    Comentario: String = String(description="Comentario ausencia", required=True)
    fecha: Date = Date(description="Fecha de ausencia", required=True)


@dataclass
class UsersResList:
    usrs: List = List(Nested(usr))


@dataclass
class Ausente:
    ausenciaid: Integer = Integer(description="ausencia id")
    fecha: Date = Date(description="Fecha ausencia reportada")
    timestamp: DateTime = DateTime(description="Fecha de registro en el sistema")
    nombres: String = String(description="Nombres usuario ausente")
    apellidos: String = String(description="Apellidos usuario ausente")
    numeroidentificacion: String = String(description="Identificacion usuario ausente")
    grado_id: Integer = Integer(description="Identificacion del grado")
    activo: Boolean = Boolean(
        description="Indica si el ususario está activo en el sistema"
    )


@dataclass
class ShowUser:
    nombres: String = String(description="User name")
    apellidos: String = String(description="User surname")
    numeroidentificacion: String = String(description="Id number")
    grado: Integer = Integer(description="User's grade id")


@dataclass
class ShowConsolidado:
    fecha: DateTime = (DateTime(description="fecha"),)
    cantidad: Integer = (Integer(description="Cantidad de usuarios"),)
