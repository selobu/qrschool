from flask_restx.fields import List, Nested
from app.apitools import createApiModelView
from app.toolsapk import Tb


qr = createApiModelView(
    "Código Qr",
    Tb.Qr,  # type: ignore
)
qr_list = createApiModelView("QrList", {"qrs": List(Nested(qr))})
qr_register = createApiModelView("Código Qr", Tb.Qr, readonlyfields=["timestamp"])  # type: ignore
qr_register_list = createApiModelView("QrList", {"qrs": List(Nested(qr_register))})
usr = createApiModelView("Usuario", Tb.User)  # type: ignore
