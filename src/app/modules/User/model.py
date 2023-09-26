# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from flask import current_app

from app.toolsapk import Base, Tb, map_name_to_table, uuidgenerator, now, gethash


# limita el uso del proyecto segun el servicio contratado
@map_name_to_table
class User(Base):
    __tablename__ = "user"
    id: Mapped[Optional[int]] = mapped_column(primary_key=True)
    # idPadre: Mapped["User"] = relationship(remote_side=["id"], backref="acudiente")
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    timestamp: Mapped[Optional[datetime]] = mapped_column(insert_default=now())
    nombres: Mapped[str] = mapped_column(String(255))
    apellidos: Mapped[str] = mapped_column(String(255))
    numeroidentificacion: Mapped[str] = mapped_column(String(255))
    fechaNacimiento: Mapped[date]
    rh: Mapped[str] = mapped_column(String(3))
    telefonoContacto: Mapped[Optional[str]] = mapped_column(String(15))
    correo: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    perfil_nombre: Mapped[Optional[int]] = mapped_column(
        ForeignKey("perfil.nombreperfil")
    )
    grado_id: Mapped[Optional[int]] = mapped_column(ForeignKey("grado.id"))
    direccion: Mapped[String] = mapped_column(String(500))
    telefono: Mapped[String] = mapped_column(String(20))
    grupoetnico_id: Mapped[Optional[int]] = mapped_column(ForeignKey("grupoetnico.id"))

    qr_id: Mapped["Qr"] = relationship(back_populates="usuario")
    password_id: Mapped["Auth"] = relationship(back_populates="usuario")

    perfil: Mapped["Perfil"] = relationship(uselist=False, back_populates="user")
    calendario: Mapped["Calendario"] = relationship(
        uselist=False, back_populates="propietario"
    )
    grado: Mapped["Grado"] = relationship(back_populates="estudiante")
    grupoetnico: Mapped["GrupoEtnico"] = relationship(back_populates="usuario")
    ausente: Mapped["Ausentismo"] = relationship(back_populates="userausente")
    docente: Mapped["Asignatura"] = relationship(back_populates="docente")
    evaluacion: Mapped["Evaluacion"] = relationship(back_populates="evaluado")

    def get_id(self):
        return self.id

    def generateqr(self, session=None):
        """Generate the qr code"""
        if self.qr_id is not None:
            return self.qr_id.code
        return Tb.Qr.register(code=uuidgenerator(), usuario_id=self.id).code

    def validatepassword(self, password):
        return gethash(password) == self.password_id.hash

    @classmethod
    def get_by_qrs(cls, qrlist: list, onlysmt=False, **kwargs):
        smts = (
            select(current_app.Tb.User)
            .join(current_app.Tb.Qr)
            .filter(current_app.Tb.Qr.code.in_(qrlist))
            .filter_by(**kwargs)
        )
        if onlysmt:
            return smts
        """Getting a list of users by given a qr list"""
        with current_app.Session() as session:
            res = session.execute(smts).all()
        return res


@map_name_to_table
class PerfilSchool(Enum):
    SIN = "SIN"
    ESTUDIANTE = "ESTUDIANTE"
    DOCENTE = "DOCENTE"
    ACUDIENTE = "ACUDIENTE"
    ADMINISTRADOR = "ADMINISTRADOR"


@map_name_to_table
class Perfil(Base):
    __tablename__ = "perfil"
    nombreperfil: Mapped[PerfilSchool] = mapped_column(primary_key=True)

    user: Mapped["User"] = relationship(back_populates="perfil")
    modulo: Mapped["PerfilModuloLnk"] = relationship(back_populates="perfil")

    def __repr__(self) -> str:
        return self.nombreperfil.value


@map_name_to_table
class Module(Base):
    __tablename__ = "module"
    modulename: Mapped[str] = mapped_column(String(200), primary_key=True)
    perfil: Mapped["PerfilModuloLnk"] = relationship(back_populates="modulo")

    def __repr__(self) -> str:
        return self.modulename


@map_name_to_table
class PerfilModuloLnk(Base):
    __tablename__ = "perfilmodulolnk"
    perfil_id: Mapped[PerfilSchool] = mapped_column(
        ForeignKey("perfil.nombreperfil"), primary_key=True
    )
    modulo_id: Mapped[str] = mapped_column(
        ForeignKey("module.modulename"), primary_key=True
    )
    has_permision: Mapped[bool] = mapped_column(Boolean, default=False)
    perfil: Mapped["Perfil"] = relationship(back_populates="modulo")
    modulo: Mapped["Module"] = relationship(back_populates="perfil")


@map_name_to_table
class GrupoEtnico(Base):
    __tablename__ = "grupoetnico"
    id: Mapped[int] = mapped_column(primary_key=True)
    grupo: Mapped[str] = mapped_column(String(200))
    usuario: Mapped["User"] = relationship(back_populates="grupoetnico")
