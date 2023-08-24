# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table


@map_name_to_table
class Matricula(Base):
    __tablename__ = "matricula"
    id: Mapped[int] = mapped_column(primary_key="True")
    anio: Mapped[int]
    periodo: Mapped[int]

    grado: Mapped["Grado"] = relationship(back_populates="matricula")


@map_name_to_table
class Grado(Base):
    __tablename__ = "grado"
    id: Mapped[int] = mapped_column(primary_key="True")
    nombre: Mapped[str] = mapped_column(String(50))
    cupomaximo: Mapped[int]
    matricula_id: Mapped[int] = mapped_column(ForeignKey("matricula.id"))
    comentariomatricula: Mapped[str] = mapped_column(String(1200))

    matricula: Mapped["Matricula"] = relationship(back_populates="grado")
    estudiante: Mapped["User"] = relationship(back_populates="grado")
    asignatura: Mapped["Asignatura"] = relationship(back_populates="grado")
