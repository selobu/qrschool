from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restx import Resource
from app.apitools import paginate_model, parser
from .pdModels import qr, usr, qr_register_list, qr_register
from .controller import QrListController, UserGetQrController, QrController

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
        return QrListController.get(parser)

    @ns_qrs.doc("Registra un codigo qr")
    @ns_qrs.expect(qr_register_list)
    @ns_qrs.marshal_list_with(qr, code=201)
    def post(self):
        """Registra un qr nuevo"""
        return QrListController.post(api.payload)


@ns_qrs.route("/usergetqr/<int:user_id>")
@ns_qrs.response(404, "Qr not found")
class UserGetQr(Resource):
    """Lee el código QR del usuario dado el id del usuario"""

    @ns_qrs.response(500, "Missing autorization header")
    @ns_qrs.doc("Información del qr dado su user_id")
    @jwt_required()
    def get(self, user_id):
        """Retorna el qr usuario"""
        return UserGetQrController.get(user_id)


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
        return QrController.put(qr_id)

    @ns_qrs.doc("Genera un nuevo código QR del usuario")
    @ns_qrs.expect(qr_register)
    @ns_qrs.marshal_with(qr)
    def put(self, qr_id):
        """Actualiza el código QR del usuario"""
        return QrController.put(qr_id, api.payload)
