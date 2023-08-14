# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table


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
