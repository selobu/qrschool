from flask import current_app as app
from flask_restx import Resource, fields
from src.config import settings
from app.apitools import createApiModel
from app.toolsapk import Tb, authorizations
from sqlalchemy import select
from flask_jwt_extended import jwt_required

api = settings.app.api
ns_qrs = api.namespace("qr", description="Gestionar códigos")

qr = createApiModel(api, Tb.Qr, "Código Qr")
qr_list = api.model("QrList", {"qrs": fields.List(fields.Nested(qr))})

qr_register = createApiModel(api, Tb.Qr, "Código Qr", readonlyfields=["timestamp"])
qr_register_list = api.model("QrList", {"qrs": fields.List(fields.Nested(qr_register))})
usr = createApiModel(api, Tb.User, "Usuario")


@ns_qrs.route("/")
class QrList(Resource):
    """Listado de qr"""

    @ns_qrs.response(500, "Missing autorization header")
    @ns_qrs.doc("Consulta el codigo qr de los usuarios")
    @ns_qrs.marshal_list_with(qr, code=200)
    @jwt_required()
    def get(self):
        """Retorna todos los qr

        límite actual 50 usuarios
        """
        with app.Session() as session:
            res = select(Tb.Qr).limit(50)
            qrs = session.execute(res).all()
        return [u[0] for u in qrs]

    if False:

        @ns_qrs.doc("Registra un codigo qr")
        @ns_qrs.expect(qr_register_list)
        @ns_qrs.marshal_list_with(qr, code=201)
        def post(self):
            """Registra un qr nuevo"""
            qrlist = api.payload["qrs"]
            # Session.begin() set automatically the commit once it takes out the with statement
            res = list()
            with app.Session.begin() as session:
                for qr in qrlist:
                    res.append(Tb.Qr.register(**qr))
                session.add_all(res)
                session.commit()
            return res


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
            usr = session.execute(user).one()[0]
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
            qr = session.execute(res).one()[0]
            return qr.usuario

    if False:

        @ns_qrs.doc("Genera un nuevo código QR del usuario")
        @ns_qrs.expect(qr_register)
        @ns_qrs.marshal_with(qr)
        def put(self, qr_id):
            """Actualiza el código QR del usuario"""
            with app.Session() as session:
                # se actualiza la información de usuario
                qr = Tb.Qr.register(id=qr_id, **api.payload)
                session.add(qr)
                session.commit()
            return qr
