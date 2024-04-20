from flask_restx.fields import List, String, Date, Integer, DateTime, Boolean, Nested
from dataclasses import dataclass
from app.apitools import createApiModelView, BaseMeta
from app.toolsapk import Tb

usr = createApiModelView("Usuario", Tb.User, readonlyfields=["active"])  # type: ignore


@dataclass
class MissingRegisterList(BaseMeta):
    ids: List = List(
        String(description="User id", required=True),
        description="Listado de identificación de usuarios",
    )
    Comentario: String = String(description="Comentario ausencia", required=True)
    fecha: Date = Date(description="Fecha de ausencia", required=True)


@dataclass
class AusentismoUsersResList(BaseMeta):
    usrs: List = List(Nested(usr))


@dataclass
class Ausente(BaseMeta):
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
class ShowUser(BaseMeta):
    nombres: String = String(description="User name")
    apellidos: String = String(description="User surname")
    numeroidentificacion: String = String(description="Id number")
    grado: Integer = Integer(description="User's grade id")


@dataclass
class AusentismoShowConsolidado(BaseMeta):
    fecha: Date = Date(description="fecha")
    cantidad: Integer = Integer(description="Cantidad de usuarios")
