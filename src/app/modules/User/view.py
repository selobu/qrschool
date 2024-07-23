from flask import current_app as app
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.apitools import FilterParams, allow_to_change_output_fmt
from .pdModels import usr_list_paginated, usr_register_list, usr
from .controller import UserListController, UserController

api = app.api  # type: ignore
ns_usrs = api.namespace("usuario", description="Gestionar usuarios")

parser = (
    FilterParams()
    .add_paginate_arguments()
    .add_outputfmt()
    .add_argument("nombres", type=str, help="name as a filter")
    .add_argument("apellidos", type=str, help="surname as a filter")
    .add_argument("grado_id", type=int, help="grado_id as an integer")
    .add_argument("numeroidentificacion", type=str, help="name as a filter")
)


@ns_usrs.route("/")
class UserList(Resource):
    """Listado de usuarios"""

    @allow_to_change_output_fmt(parser, keyword="usrs")
    @ns_usrs.doc("Consulta la información de usuario")
    @ns_usrs.marshal_with(usr_list_paginated, code=200)
    @ns_usrs.expect(parser.paginate_model)
    @jwt_required()
    def get(self):
        """Retorna todos los usuarios
        límite actual 50 usuarios
        """
        return UserListController.get(parser)

    @ns_usrs.doc("Registra un usuario")
    @ns_usrs.expect(usr_register_list)
    @ns_usrs.marshal_list_with(usr, code=201)
    @ns_usrs.response(400, "Can't create the new user")
    def post(self):
        """Registra un usuario nuevo"""
        return UserListController.post(api.payload)


@ns_usrs.route("/<int:user_id>")
@ns_usrs.response(404, "User not found")
class User(Resource):
    """Usuario administracion"""

    @ns_usrs.doc("Información del usuario dado su id")
    @ns_usrs.marshal_with(usr)
    @jwt_required()
    def get(self, user_id):
        """Retorna la información del usuario"""
        return UserController.get(user_id)

    @ns_usrs.doc("Actualiza la información del usuario")
    @ns_usrs.expect(usr)
    @ns_usrs.marshal_with(usr)
    @jwt_required()
    def put(self, user_id):
        """Actualiza la información de un usuario"""
        return UserController.put(user_id, api.payload)
