# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum

from app.toolsapk import Base, Tb, map_name_to_table, uuidgenerator, now


# limita el uso del proyecto segun el servicio contratado
@map_name_to_table
class User(Base):
    __tablename__ = "user"
    id: Mapped[Optional[int]] = mapped_column(primary_key=True)
    # idPadre: Mapped["User"] = relationship(remote_side=["id"], backref="acudiente")
    active: Mapped[bool] = mapped_column(Boolean, default=False)
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

    def generateqr(self, session=None):
        """Generate the qr code"""
        if self.qr_id is not None:
            return self.qr_id
        return Tb.Qr.register(code=uuidgenerator())


class PerfilSchool(Enum):
    ESTUDIANTE = "estudiante"
    DOCENTE = "docente"
    ACUDIENTE = "acudiente"
    ADMINISTRADOR = "administrador"


@map_name_to_table
class Perfil(Base):
    __tablename__ = "perfil"
    nombreperfil: Mapped[PerfilSchool] = mapped_column(primary_key=True)

    user: Mapped["User"] = relationship(back_populates="perfil")
    modulo: Mapped["PerfilModuloLnk"] = relationship(back_populates="perfil")


@map_name_to_table
class Module(Base):
    __tablename__ = "module"
    modulename: Mapped[str] = mapped_column(String(200), primary_key=True)
    perfil: Mapped["PerfilModuloLnk"] = relationship(back_populates="modulo")


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
