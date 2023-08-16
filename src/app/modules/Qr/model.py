# coding:utf-8
# from flask_sqlalchemy import sqlalchemy
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.toolsapk import Base, map_name_to_table


# limita el uso del proyecto segun el servicio contratado
@map_name_to_table
class Qr(Base):
    __tablename__ = "qr"
    id: Mapped[Optional[int]] = mapped_column(primary_key=True)
    timestamp: Mapped[Optional[datetime]] = mapped_column(insert_default=func.now())
    code: Mapped[str] = mapped_column(String(55))

    usuario_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    usuario: Mapped["User"] = relationship(back_populates="qr_id")
