from dataclasses import dataclass
from flask_restx.fields import String, Boolean, List


@dataclass
class Auth:
    email: String = String(description="direccion de correo registrado")
    password: String = String(description="Contraseña")


@dataclass
class LoginResponse:
    status: String = String(description="estado de la autenticacion")
    auth: Boolean = Boolean(description="está autenticado?")
    fresh_access_token: String = String(description="fresh access token")
    access_token: String = String(description="Access token")
    email: String = String(description="direccion de correo registrado")
    username: String = String(description="Nombre del usario")
    qr: String = String(description="Código QR del usuario")
    active: Boolean = Boolean(
        description="Indica si el usuario está activo en la plataforma"
    )
    modules: List = List(String(description="Modulo con permiso"))
