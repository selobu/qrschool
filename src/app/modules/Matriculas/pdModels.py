from app.apitools import BaseMeta, createApiModelView
from flask_restx.fields import List, Nested, String
from dataclasses import dataclass
from app.toolsapk import Tb

grado = createApiModelView("Grado", Tb.Grado)  # type: ignore
grado_register = createApiModelView("CodigoGrado", Tb.Grado)  # type: ignore
matricula = createApiModelView("Matricula", Tb.Matricula)  # type: ignore
matricula_register = createApiModelView(
    "CodigoMatricula",
    Tb.Matricula,  # type: ignore
    readonlyfields=["grado"],
)
usr = createApiModelView("Usuario", Tb.User)  # type: ignore


@dataclass
class GradoLista(BaseMeta):
    grados: List = List(Nested(grado))


@dataclass
class GradoListaRegister(BaseMeta):
    grados: List = List(Nested(grado_register))


@dataclass
class MatriculaList(BaseMeta):
    matriculas: List = List(Nested(matricula))


@dataclass
class MatriculaRegisterList(BaseMeta):
    matriculas: List = List(Nested(matricula_register))


@dataclass
class MatriculaQrRegisterList(BaseMeta):
    qrs: List = List(String(required=True))


grado_list = GradoLista().get_model()
grado_register_list = GradoListaRegister().get_model()
matricula_list = MatriculaList().get_model()
matricula_register_list = MatriculaRegisterList().get_model()
qr_users_list = MatriculaQrRegisterList().get_model()
