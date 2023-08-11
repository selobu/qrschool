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


# limita el uso del proyecto segun el servicio contratado
@map_name_to_table
class Calendario(Base):
    __tablename__ = "calendario"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255))
    Desripcion: Mapped[Optional[str]] = mapped_column(String(1200))
    propietario_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    propietario: Mapped["User"] = relationship(back_populates="calendario")
    evento: Mapped["Evento"] = relationship(
        back_populates="calendario"
    )


@map_name_to_table
class Evento(Base):
    __tablename__ = "evento"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    titulo: Mapped[str] = mapped_column(String(255))
    fechaHora: Mapped[date]
    invitados: Mapped[str] = mapped_column(String(1200))  # Json DATA?
    ubicacion: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str] = mapped_column(String(1200))
    calendario_id: Mapped[int] = mapped_column(ForeignKey("calendario.id"))

    calendario: Mapped["Calendario"] = relationship(back_populates="evento")
    notificacion: Mapped["NotificacionEventos"] = relationship(back_populates="evento")


@map_name_to_table
class NotificacionEventos(Base):
    __tablename__ = "notificacioneventos"
    id: Mapped[int] = mapped_column(primary_key=True)
    tiempoantes: Mapped[int]  #
    lineatiempo: Mapped[str] = mapped_column(String(50))  # minutos|horas|dias|semanas
    evento_id: Mapped[int] = mapped_column(ForeignKey("evento.id"))

    evento: Mapped["Evento"] = relationship(back_populates="notificacion")
