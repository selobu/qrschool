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
class Auth(Base):
    __tablename__ = "auth"
    usuario_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[Optional[datetime]] = mapped_column(default=now)
    hash: Mapped[str] = mapped_column(String(100))

    usuario: Mapped["User"] = relationship(back_populates="password_id")
