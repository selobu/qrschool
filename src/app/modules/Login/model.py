# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table, now


# limita el uso del proyecto segun el servicio contratado
@map_name_to_table
class Auth(Base):
    __tablename__ = "auth"
    usuario_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    timestamp: Mapped[Optional[datetime]] = mapped_column(default=now)
    hash: Mapped[str] = mapped_column(String(100))

    usuario: Mapped["User"] = relationship(back_populates="password_id")
