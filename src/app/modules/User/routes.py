from flask import current_app as app
from flask_restx import Resource, fields
from sqlalchemy import select
from flask_jwt_extended import jwt_required

from app.apitools import createApiModel, ParserModel, Argument, changeoutputfmt
from app.toolsapk import Tb, gethash, uuidgenerator

api = app.api  # type: ignore
ns_usrs = api.namespace("usuario", description="Gestionar usuarios")

usr = createApiModel(api, Tb.User, "Usuario", readonlyfields=["active"])  # type: ignore
usr_post = createApiModel(
    api,
    Tb.User,  # type: ignore
    "Usuario",
    readonlyfields=[
        "timestamp",
        "perfil_id",
        "grado_id",
        "grupoetnico_id",
        "is_active",
        "perfil_nombre",
    ],
    additionalfields={
        "password": fields.String(
            description="contraseña", required=True, min_length=9, default="***"
        )
    },
)

usr_register_list = api.model(
    "UsersResList", {"usrs": fields.List(fields.Nested(usr_post))}
)

usr_list_paginated = api.model(
    "UsersResListPag", {"usrs": fields.List(fields.Nested(usr))}
)

parser = ParserModel()
user_paginate_model = (
    parser.add_paginate_arguments()
    .add_outputfmt()
    .add_argument(
        Argument(
            name="nombres",
            type=str,
            help="name as a filter - optional",
            required=False,
        )
    )
    .add_argument(
        Argument(
            name="apellidos",
            type=str,
            help="surname as a filter - optional",
            required=False,
        )
    )
    .add_argument(
        Argument(
            name="grado_id",
            type=int,
            help="grado_id as an integer - optional",
            required=False,
        )
    )
    .add_argument(
        Argument(
            name="numeroidentificacion",
            type=str,
            help="name as a filter - optional",
            required=False,
        )
    )
    .paginate_model
)


@ns_usrs.route("/")
class UserList(Resource):
    """Listado de usuarios"""

    @changeoutputfmt(parser, keyword="usrs")
    @ns_usrs.doc("Consulta la información de usuario")
    @ns_usrs.marshal_with(usr_list_paginated, code=200)
    @ns_usrs.expect(user_paginate_model)
    @jwt_required()
    def get(self):
        """Retorna todos los usuarios
        límite actual 50 usuarios
        """
        parser.parseargs()
        page = parser.get("page", default=1)
        per_page = parser.get("per_page", default=app.config["PER_PAGE"])
        params = {
            "nombres": parser.get("nombres", None),
            "apellidos": parser.get("apellidos", None),
            "grado_id": parser.get("grado_id", None),
            "numeroidentificacion": parser.get("numeroidentificacion", None),
        }
        with app.Session() as session:
            q = select(Tb.User)
            for key, value in params.items():
                if value is None:
                    continue
                tipe = parser[key].type
                if str(tipe) == str(str):
                    q = q.filter(getattr(Tb.User, key).like(f"%{value.lower()}%"))
                elif str(tipe) == str(int):
                    q = q.filter(getattr(Tb.User, key) == value)
            q = (
                q.order_by(Tb.User.correo.asc())
                .limit(per_page)
                .offset(per_page * (page - 1))
            )
            return {"usrs": session.scalars(q).all()}

    @ns_usrs.doc("Registra un usuario")
    @ns_usrs.expect(usr_register_list)
    @ns_usrs.marshal_list_with(usr, code=201)
    def post(self):
        """Registra un usuario nuevo"""
        userlist = api.payload
        # Session.begin() set automatically the commit once it takes out the with statement
        res = list()
        with app.Session() as session:
            for user in userlist:
                res.append(Tb.User.register(**user))
            session.add_all(res)
            session.commit()
        with app.Session() as session:
            # Se generan los códigos qr de todos los usuarios agregados y se registra la contraseña
            qrs = list()
            passwords = list()
            for user in res:
                qrs.append(Tb.Qr.register(usuario_id=user.id, code=uuidgenerator()))
                passwords.append(
                    Tb.Auth.register(hash=gethash(user.password), usuario_id=user.id)
                )
            session.add_all(qrs)
            session.add_all(passwords)
            session.commit()
        return res


@ns_usrs.route("/<int:user_id>")
@ns_usrs.response(404, "User not found")
class User(Resource):
    """Usuario administracion"""

    @ns_usrs.doc("Información del usuario dado su id")
    @ns_usrs.marshal_with(usr)
    @jwt_required()
    def get(self, user_id):
        """Retorna la información del usuario"""
        with app.Session() as session:
            res = select(Tb.User).filter(Tb.User.id == user_id)
            return session.scalars(res).one()

    @ns_usrs.doc("Actualiza la información del usuario")
    @ns_usrs.expect(usr)
    @ns_usrs.marshal_with(usr)
    @jwt_required()
    def put(self, user_id):
        """Actualiza la información de un usuario"""
        with app.Session() as session:
            # se actualiza la información de usuario
            user = Tb.User.register(id=user_id, **api.payload)
            session.add(user)
            session.commit()
        return user
