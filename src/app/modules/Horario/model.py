# coding:utf-8
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table


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
