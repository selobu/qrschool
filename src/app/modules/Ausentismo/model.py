# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from datetime import date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table


@map_name_to_table
class Ausentismo(Base):
    __tablename__ = "ausentismo"
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date]
    timestamp: Mapped[datetime]
    userausente_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    responsableRegistro: Mapped[str] = mapped_column(String(200))
    comentario: Mapped[str] = mapped_column(String(1200))
    userausente: Mapped["User"] = relationship(back_populates="ausente")
