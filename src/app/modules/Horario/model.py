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
class Horario(Base):
    __tablename__ = "horario"
    id: Mapped[int] = mapped_column(primary_key=True)
    diasemana: Mapped[int]  # domingo día 1
    horaInicio: Mapped[int]
    minutoInicio: Mapped[int]
    horaFinal: Mapped[int]
    minutoFinal: Mapped[int]
    asignatura_id: Mapped[int] = mapped_column(ForeignKey("asignatura.id"))

    asignatura: Mapped["Asignatura"] = relationship(back_populates="horario")
