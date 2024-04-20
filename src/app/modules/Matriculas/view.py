# coding:utf-8

from flask_jwt_extended import jwt_required
from flask_restx import Resource
from sqlalchemy import select
from flask import current_app
from app.apitools import (
    get_model_list,
    post_model_list,
    get_model,
    put_model,
)
from app.toolsapk import Tb
from .pdModels import (
    matricula,
    matricula_register_list,
    matricula_register,
    grado,
    grado_register_list,
    grado_register,
    usr,
    qr_users_list,
)

api = current_app.api  # type: ignore
ns_matricula = api.namespace("matricula", description="Gestionar matriculas")


@ns_matricula.route("/")
class MatriculaList(Resource):
    """Listado de matriculas"""

    @ns_matricula.response(500, "Missing autorization header")
    @ns_matricula.doc("Consulta todos los periodos de matrícula")
    @ns_matricula.marshal_list_with(matricula, code=200)
    @jwt_required()
    @get_model_list(Tb.Matricula, limit=50)  # type: ignore
    def get(self):
        """Consulta todos los perídos de matrícula"""

    @ns_matricula.doc("Registra uno o mas procesos de matrículas")
    @ns_matricula.expect(matricula_register_list)
    @ns_matricula.marshal_list_with(matricula, code=200)
    @jwt_required()
    @post_model_list(payload="matriculas", model=Tb.Matricula)  # type: ignore
    def post(self):
        """Registra uno o mas procesos de matrículas"""


@ns_matricula.route("/<int:id>")
class Matricula(Resource):
    """Consulta y modifica una matricula"""

    @ns_matricula.response(500, "Missing autorization header")
    @ns_matricula.doc("Consulta una matrícula")
    @ns_matricula.marshal_list_with(matricula, code=200)
    @jwt_required()
    @get_model(Tb.Matricula)  # type: ignore
    def get(self, id):
        """Consulta una matrícula"""

    @ns_matricula.doc("Registra o actualiza matrículas")
    @ns_matricula.expect(matricula_register)
    @ns_matricula.marshal_with(matricula, code=200)
    @jwt_required()
    @put_model(model=Tb.Matricula)  # type: ignore
    def put(self, id):
        """Actualiza una matricula"""


@ns_matricula.route("/grado/")
class GradoList(Resource):
    """Listado de grados"""

    @ns_matricula.response(500, "Missing autorization header")
    @ns_matricula.doc("Consulta todos los grados")
    @ns_matricula.marshal_list_with(grado, code=200)
    @jwt_required()
    @get_model_list(Tb.Grado, limit=50)  # type: ignore
    def get(self):
        """Retorna todos los grados

        límite actual 50 grados
        """

    @ns_matricula.doc("Registra uno o mas grados")
    @ns_matricula.expect(grado_register_list)
    @ns_matricula.marshal_list_with(grado, code=201)
    @jwt_required()
    @post_model_list(payload="grados", model=Tb.Grado)  # type: ignore
    def post(self):
        """Registra uno o mas grados"""


@ns_matricula.route("/grado/<int:id>")
class GradoElement(Resource):
    """Listado de grado"""

    @ns_matricula.response(500, "Missing autorization header")
    @ns_matricula.doc("Consulta un grado")
    @ns_matricula.marshal_with(grado, code=200)
    @jwt_required()
    @get_model(Tb.Grado)  # type: ignore
    def get(self, id):
        """Consulta un grado"""

    @ns_matricula.doc("Modifica uno grado")
    @ns_matricula.expect(grado_register)
    @ns_matricula.marshal_with(grado, code=201)
    @put_model(model=Tb.Grado)  # type: ignore
    def put(self, id):
        """Modifica uno grado"""


@ns_matricula.route("/grado/users/<int:gradoid>/")
class GradoUsers(Resource):
    """Listado de estudiantes"""

    @ns_matricula.response(500, "Missing autorization header")
    @ns_matricula.doc("Consulta el listado de estudiantes de un grado")
    @ns_matricula.marshal_list_with(usr, code=200)
    @jwt_required()
    def get(self, gradoid):
        """Consulta el listado de estudiantes de un grado"""
        with current_app.Session() as session:
            smts = select(Tb.User).join(Tb.Grado).filter(Tb.Grado.id == gradoid)
            return session.scalars(smts).all()

    @ns_matricula.doc("Registra un listado de estudiantes de un grado")
    @ns_matricula.expect(qr_users_list)
    @ns_matricula.marshal_list_with(usr, code=201)
    @jwt_required()
    def post(self, gradoid):
        """Registra un listado de estudiantes de un grado"""
        qrs = api.payload["qrs"]
        # se consulta los usuarios
        userssmts = Tb.User.get_by_qrs(qrs, onlysmt=True)
        # se asocian los usuarios al grado
        with current_app.Session() as session:
            users = session.scalars(userssmts).all()
            smts = select(current_app.Tb.Grado).filter_by(id=gradoid)
            grado = session.scalars(smts).one()
            res = list(grado.estudiante)
            res.extend(users)
            grado.estudiante = list(set(res))
            session.commit()
        return users

    @ns_matricula.doc("Elimina el listado de estudiantes de un grado")
    @ns_matricula.expect(grado_register)
    @ns_matricula.marshal_with(grado, code=201)
    @jwt_required()
    def delete(self, gradoid):
        """Elimina el listado de estudiantes de un grado"""
        ...
