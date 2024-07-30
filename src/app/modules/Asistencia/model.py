# coding:utf-8
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table, now


@map_name_to_table
class Asistencia(Base):
    __tablename__ = "asistencia"
    id: Mapped[Optional[int]] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True
    )
    timestamp: Mapped[Optional[datetime]] = mapped_column(insert_default=now())

    userasistencia: Mapped["UsrAsistenciaLnk"] = relationship(
        back_populates="asistencia", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Asistencia> {self.id} {self.timestamp}"


@map_name_to_table
class UsrAsistenciaLnk(Base):
    __tablename__ = "userasistencia"
    asistencia_id: Mapped[int] = mapped_column(
        ForeignKey("asistencia.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True, nullable=False
    )
    asistencia: Mapped["Asistencia"] = relationship(
        back_populates="userasistencia",
    )
    user: Mapped["User"] = relationship(
        back_populates="asistencia",
    )
