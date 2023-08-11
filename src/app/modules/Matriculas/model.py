# coding:utf-8
from app.toolsapk import db, Tb
from app.toolsapk import map_name_to_table
from app.toolsapk import uuidgenerator, now, Base
from flask import url_for, abort
from typing import Optional

# from flask_sqlalchemy import sqlalchemy
from datetime import timedelta, date, datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


@map_name_to_table
class Matricula(Base):
    __tablename__ = "matricula"
    id: Mapped[int] = mapped_column(primary_key="True")
    anio: Mapped[int]
    periodo: Mapped[int]

    grado: Mapped["Grado"] = relationship(back_populates="matricula")


@map_name_to_table
class Grado(Base):
    __tablename__ = "grado"
    id: Mapped[int] = mapped_column(primary_key="True")
    nombre: Mapped[str] = mapped_column(String(50))
    cupomaximo: Mapped[int]
    matricula_id: Mapped[int] = mapped_column(ForeignKey("matricula.id"))
    matriculado: Mapped[bool]
    comentariomatricula: Mapped[str] = mapped_column(String(1200))

    matricula: Mapped["Matricula"] = relationship(back_populates="grado")
    estudiante: Mapped["User"] = relationship(back_populates="grado")
    asignatura: Mapped["Asignatura"] = relationship(back_populates="grado")
