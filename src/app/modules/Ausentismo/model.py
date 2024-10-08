# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from datetime import date, datetime
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.toolsapk import Base, map_name_to_table, now


@map_name_to_table
class Ausentismo(Base):
    __tablename__ = "ausentismo"
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date]
    timestamp: Mapped[Optional[datetime]] = mapped_column(insert_default=now())
    userausente_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    responsableRegistro: Mapped[str] = mapped_column(String(200))
    comentario: Mapped[str] = mapped_column(String(1200))

    # -----------
    # ORM Relationships
    # ------------
    userausente: Mapped["User"] = relationship(back_populates="ausente")
    user_name: AssociationProxy[str] = association_proxy("userausente", "nombres")
    user_lastname: AssociationProxy[str] = association_proxy("userausente", "apellidos")
    user_grade_id: AssociationProxy[str] = association_proxy("userausente", "grado_id")
    # user_grade_name: AssociationProxy[str] = association_proxy("user_grade", "nombre")
