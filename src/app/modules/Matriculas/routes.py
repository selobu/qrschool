# coding:utf-8

from flask_jwt_extended import jwt_required
from flask_restx import Resource, fields

from app.apitools import (
    createApiModel,
    get_model_list,
    post_model_list,
    get_model,
    put_model,
)
from app.config import settings
from app.toolsapk import Tb

api = settings.app.api  # type: ignore
ns_grado = api.namespace("Matricula", description="Gestionar matriculas y grados")

grado = createApiModel(api, Tb.Grado, "Grado")  # type: ignore
grado_list = api.model("GradoList", {"grados": fields.List(fields.Nested(grado))})


grado_register = createApiModel(
    api,
    Tb.Grado,  # type: ignore
    "CodigoGrado",
)
grado_register_list = api.model(
    "GradoList", {"grados": fields.List(fields.Nested(grado_register))}
)

matricula = createApiModel(api, Tb.Matricula, "Matricula")  # type: ignore
matricula_list = api.model(
    "MatriculaList", {"matriculas": fields.List(fields.Nested(matricula))}
)

matricula_register = createApiModel(
    api,
    Tb.Matricula,  # type: ignore
    "CodigoMatricula",
    readonlyfields=["grado"],
)

matricula_register_list = api.model(
    "MatriculaList", {"matriculas": fields.List(fields.Nested(matricula_register))}
)


@ns_grado.route("/")
class MatriculaList(Resource):
    """Listado de matriculas"""

    @ns_grado.response(500, "Missing autorization header")
    @ns_grado.doc("Consulta todos los periodos de matrícula")
    @ns_grado.marshal_list_with(matricula, code=200)
    @jwt_required()
    @get_model_list(Tb.Matricula, limit=50)  # type: ignore
    def get(self):
        """Consulta todos los perídos de matrícula"""

    @ns_grado.doc("Registra uno o mas procesos de matrículas")
    @ns_grado.expect(matricula_register_list)
    @ns_grado.marshal_list_with(matricula, code=200)
    @jwt_required()
    @post_model_list(payload="matriculas", model=Tb.Matricula)  # type: ignore
    def post(self):
        """Registra uno o mas procesos de matrículas"""


@ns_grado.route("/<int:id>")
class Matricula(Resource):
    """Consulta y modifica una matricula"""

    @ns_grado.response(500, "Missing autorization header")
    @ns_grado.doc("Consulta una matrícula")
    @ns_grado.marshal_list_with(matricula, code=200)
    @jwt_required()
    @get_model(Tb.Matricula)  # type: ignore
    def get(self, id):
        """Consulta una matrícula"""

    @ns_grado.doc("Registra o actualiza matrículas")
    @ns_grado.expect(matricula_register)
    @ns_grado.marshal_with(matricula, code=200)
    @jwt_required()
    @put_model(model=Tb.Matricula)  # type: ignore
    def put(self, id):
        """Actualiza una matricula"""


@ns_grado.route("/grado/")
class GradoList(Resource):
    """Listado de grado"""

    @ns_grado.response(500, "Missing autorization header")
    @ns_grado.doc("Consulta todos los grados")
    @ns_grado.marshal_list_with(grado, code=200)
    @jwt_required()
    @get_model_list(Tb.Grado, limit=50)  # type: ignore
    def get(self):
        """Retorna todos los grados

        límite actual 50 grados
        """

    @ns_grado.doc("Registra uno o mas grados")
    @ns_grado.expect(grado_register_list)
    @ns_grado.marshal_list_with(grado, code=201)
    @jwt_required()
    @post_model_list(payload="grados", model=Tb.Grado)  # type: ignore
    def post(self):
        """Registra uno o mas grados"""


@ns_grado.route("/grado/<int:id>")
class Grado(Resource):
    """Listado de grado"""

    @ns_grado.response(500, "Missing autorization header")
    @ns_grado.doc("Consulta todos los grados")
    @ns_grado.marshal_with(grado, code=200)
    @jwt_required()
    @get_model(Tb.Grado)  # type: ignore
    def get(self, id):
        """Consulta un grado"""

    @ns_grado.doc("Registra uno o mas grados")
    @ns_grado.expect(grado_register)
    @ns_grado.marshal_with(grado, code=201)
    @put_model(model=Tb.Grado)  # type: ignore
    def put(self, id):
        """Actualiza un grado"""
