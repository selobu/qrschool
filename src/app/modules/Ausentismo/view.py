from flask import current_app as app
from app.apitools import createApiModel, FilterParams, allow_to_change_output_fmt
from flask_restx import fields
from app.toolsapk import Tb
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .controller import AusenciaController, AusenciaLast7Controller

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


query_params = (
    FilterParams()
    .add_paginate_arguments()
    .add_outputfmt()
    .add_argument("nombres", type=str, help="name as a filter")
    .add_argument("apellidos", type=str, help="surname as a filter")
    .add_argument("grado_id", type=int, help="grado_id as an integer")
    .add_argument("numeroidentificacion", type=str, help="id number as a filter")
    .add_argument("fecha", type=str, help="date formated as iso 8601")
)


@ns_ausencia.route("/")
class ausenciaList(Resource):
    """Listado de usuarios"""

    @allow_to_change_output_fmt(query_params)
    @ns_ausencia.response(500, "Missing autorization header")
    @ns_ausencia.doc("Retorna los listados de ausencia paginados")
    @ns_ausencia.marshal_list_with(ausente, code=200)
    @ns_ausencia.expect(query_params.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna los listados de ausencia paginados"""
        return AusenciaController.get(query_params)

    @ns_ausencia.doc("Registra ausencia de un usuario")
    @ns_ausencia.expect(ausencia_register_list)
    @ns_ausencia.response(200, "success")
    @jwt_required()
    def post(self):
        """Registra ausencia de un usuario"""
        return AusenciaController.post(app.api)


@ns_ausencia.route("/last7/")
class AusenciaLast7(Resource):
    """Listado de ausencia"""

    @ns_ausencia.response(500, "Missing autorization header")
    @ns_ausencia.doc("Retorna la ausencia de los ultimos 7 días")
    @ns_ausencia.marshal_list_with(showconsolidado, code=200)
    @jwt_required()
    def get(self):
        """Retorna ausencia de los ultimos 7 días"""
        return AusenciaLast7Controller.get()
