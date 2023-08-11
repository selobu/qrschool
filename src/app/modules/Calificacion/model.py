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
class Evaluacion(Base):
    __tablename__ = "evaluacion"
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date]
    resultado: Mapped[int]
    comentario: Mapped[str] = mapped_column(String(800))
    aprobado: Mapped[bool]
    periodo: Mapped[int]
    evaluado_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    evaluado: Mapped["User"] = relationship(back_populates="evaluacion")
