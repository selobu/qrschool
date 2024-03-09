from flask import current_app as app
from app.apitools import FilterParams, allow_to_change_output_fmt, get_pyd_model
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .controller import AusenciaController, AusenciaLast7Controller
from .pdModels import (
    MissingRegisterList,
    UsersResList,
    Ausente,
    ShowUser,
    ShowConsolidado,
)

ns_ausencia = app.api.namespace(
    "ausencia", description="Registrar ausencia de usuarios"
)

ausencia_register_list = get_pyd_model(MissingRegisterList)
usr_list_paginated = get_pyd_model(UsersResList)
ausente = get_pyd_model(Ausente)
showuser = get_pyd_model(ShowUser)
showconsolidado = get_pyd_model(ShowConsolidado)


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
