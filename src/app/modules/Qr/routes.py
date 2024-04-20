from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from sqlalchemy import select
from app.apitools import paginate_model, parser
from app.toolsapk import Tb
from .pdModels import qr, usr

api = app.api  # type: ignore
ns_qrs = api.namespace("qr", description="Gestionar códigos")


@ns_qrs.route("/")
class QrList(Resource):
    """Listado de qr"""

    @ns_qrs.response(500, "Missing autorization header")
    @ns_qrs.doc("Consulta el codigo qr de los usuarios")
    @ns_qrs.marshal_list_with(qr, code=200)
    @ns_qrs.expect(paginate_model)
    @jwt_required()
    def get(self):
        """Retorna todos los qr"""
        page = parser.get("page", default=1)
        per_page = parser.get("per_page", default=app.config["PER_PAGE"])
        with app.Session() as session:
            q = (
                select(Tb.Qr)
                .order_by(Tb.Qr.id.asc())
                .limit(per_page)
                .offset(per_page * (page - 1))
            )
            return session.scalars(q).all()

    # if False:

    #     @ns_qrs.doc("Registra un codigo qr")
    #     @ns_qrs.expect(qr_register_list)
    #     @ns_qrs.marshal_list_with(qr, code=201)
    #     def post(self):
    #         """Registra un qr nuevo"""
    #         qrlist = api.payload["qrs"]
    #         # Session.begin() set automatically the commit once it takes out the with statement
    #         res = list()
    #         with app.Session.begin() as session:
    #             for qr in qrlist:
    #                 res.append(Tb.Qr.register(**qr))
    #             session.add_all(res)
    #             session.commit()
    #         return res


@ns_qrs.route("/usergetqr/<int:user_id>")
@ns_qrs.response(404, "Qr not found")
class UserGetQr(Resource):
    """Lee el código QR del usuario dado el id del usuario"""

    @ns_qrs.response(500, "Missing autorization header")
    @ns_qrs.doc("Información del qr dado su user_id")
    @jwt_required()
    def get(self, user_id):
        """Retorna el qr usuario"""
        with app.Session() as session:
            # Se verifica que el usuario exista
            user = select(Tb.User).filter(Tb.User.id == user_id)
            usr = session.scalars(user).one()
            if usr.qr_id is None:
                # se genera un nuevo código QR
                qr = usr.generateqr()
                qr.usuario = usr
                session.add(qr)
                session.commit()
            return usr.qr_id.code


@ns_qrs.route("/<string:qr_id>")
@ns_qrs.response(404, "Qr not found")
class Qr(Resource):
    """Qr administracion"""

    @ns_qrs.response(500, "Missing autorization header")
    @ns_qrs.doc("Información del qr")
    @ns_qrs.marshal_with(usr)
    @jwt_required()
    def get(self, qr_id):
        """Retorna los datos del usuario"""
        with app.Session() as session:
            res = select(Tb.Qr).join(Tb.Qr.usuario).filter(Tb.Qr.code == qr_id)
            qr = session.scalars(res).one()
            return qr.usuario

    # if False:

    #     @ns_qrs.doc("Genera un nuevo código QR del usuario")
    #     @ns_qrs.expect(qr_register)
    #     @ns_qrs.marshal_with(qr)
    #     def put(self, qr_id):
    #         """Actualiza el código QR del usuario"""
    #         with app.Session() as session:
    #             # se actualiza la información de usuario
    #             qr = Tb.Qr.register(id=qr_id, **api.payload)
    #             session.add(qr)
    #             session.commit()
    #         return qr
