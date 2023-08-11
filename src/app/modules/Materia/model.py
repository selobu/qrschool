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
class Asignatura(Base):
    __tablename__ = "asignatura"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255))
    grado_id: Mapped[int] = mapped_column(ForeignKey("grado.id"))
    docente_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    grado: Mapped["Grado"] = relationship(back_populates="asignatura")
    docente: Mapped["User"] = relationship(back_populates="docente")
    horario: Mapped["Horario"] = relationship(back_populates="asignatura")
