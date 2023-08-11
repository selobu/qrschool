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
class Qr(Base):
    __tablename__ = "qr"
    id: Mapped[Optional[int]] = mapped_column(primary_key=True)
    timestamp: Mapped[Optional[datetime]] = mapped_column(default=now)
    code: Mapped[str] = mapped_column(String(55))

    usuario_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    usuario: Mapped["User"] = relationship(back_populates="qr_id")
