from flask import current_app as app
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from app.apitools import FilterParams, allow_to_change_output_fmt, get_pyd_model

from .controller import (
    AsistenciaListController,
    AsistenciaController,
    AsistenciaLast7Controller,
)
from .pdModels import (
    QrRegisterList,
    AsistenciaModel,
    Showuser,
    ShowConsolidado,
    UsersResList,
)

qr_register_list = get_pyd_model(QrRegisterList)
asistencia = get_pyd_model(AsistenciaModel)
showuser = get_pyd_model(Showuser)
showconsolidado = get_pyd_model(ShowConsolidado)
usr_list_paginated = get_pyd_model(UsersResList)

ns_asistencia = app.api.namespace(
    "asistencia", description="Registrar asistencia de usuarios"
)

parser = (
    FilterParams()
    .add_paginate_arguments()
    .add_outputfmt()
    .add_argument("id", type=str, help="name asistencia filter")
    .add_argument("timestamp", type=str, help="datetime")
)

parseroutput = FilterParams().add_outputfmt()


@ns_asistencia.route("/")
class AsistenciaList(Resource):
    """Listado de usuarios"""

    @allow_to_change_output_fmt(parser)
    @ns_asistencia.response(500, "Missing autorization header")
    @ns_asistencia.doc("Consulta el codigo qr de los usuarios")
    @ns_asistencia.marshal_list_with(asistencia, code=200)
    @ns_asistencia.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna los listados de asistencia paginados"""
        return AsistenciaListController.get(parser)

    @ns_asistencia.doc("Registra un usuario")
    @ns_asistencia.expect(qr_register_list)
    @ns_asistencia.marshal_with(asistencia, code=200)
    @jwt_required()
    def post(self):
        """Registra listado de asistencia"""
        return AsistenciaListController.post(app.api)


@ns_asistencia.route("/<int:asistencia_id>/")
class Asistencia(Resource):
    """Listado de asistencia"""

    @allow_to_change_output_fmt(parser)
    @ns_asistencia.response(500, "Missing autorization header")
    @ns_asistencia.doc("Retorna el listado de asistentes paginados")
    @ns_asistencia.marshal_list_with(showuser, code=200)
    @ns_asistencia.expect(parser.paginate_model)
    @jwt_required()
    def get(self, asistencia_id):
        """Retorna los asistentes paginados"""
        return AsistenciaController.get(parser, asistencia_id)


@ns_asistencia.route("/last7/")
class AsistenciaLast7(Resource):
    """Listado de asistencia ultimos 7"""

    @allow_to_change_output_fmt(parseroutput)
    @ns_asistencia.response(500, "Missing autorization header")
    @ns_asistencia.doc("Retorna asistencia de los ultimos 7 días")
    @ns_asistencia.marshal_with(showconsolidado, code=200)
    @ns_asistencia.expect(parseroutput.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna asistencia de los ultimos 7 días"""
        return AsistenciaLast7Controller.get()
