# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table


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
