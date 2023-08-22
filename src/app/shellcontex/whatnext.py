# coding:utf-8
__all__ = ["whatnext"]

from flask import current_app as app
from app.toolsapk import map_name_to_shell
from sqlalchemy import select
from app.toolsapk import shell_decorated
from app.modules.User.model import PerfilSchool


@map_name_to_shell
def whatnext():
    # check if tables exists
    table_created = input("Do you want to create tables? y/n [n]: ")
    if table_created.lower() in ("y", "yes"):
        shell_decorated["createdb"]()
    # check if profiles exist
    with app.Session() as session:
        res = select(app.Tb.Perfil.nombreperfil).limit(20)
        registerd = [r[0].value for r in session.execute(res).all()]
        print(f"registerd {registerd}")
        missing = [
            perfil.value
            for perfil in list(PerfilSchool)
            if perfil.value not in registerd
        ]
    update_profile = False
    if len(missing) > 0:
        update_profile = input("Desea actualizar los perfiles? y/n [n]: ")
    else:
        print("all profiles are registered!")
    if update_profile:
        with app.Session() as session:
            session.add_all(
                [app.Tb.Perfil.register(nombreperfil=miss) for miss in missing]
            )
            session.commit()
    # Check if admin exist
    with app.Session() as session:
        res = (
            select(app.Tb.User.id)
            .join(app.Tb.Perfil)
            .where(app.Tb.Perfil.nombreperfil == "ADMINISTRADOR")
        )
        cantidadadministradores = session.execute(func.count(res)).scalar()

    agregaradmin = False
    if cantidadadministradores == 0:
        agregaradmin = input(
            "No se detectaron usuarios administadores, desea agregar uno? y/n [n]: "
        )
    if agregaradmin in ("y", "yes"):
        shell_decorated["registeradmin"]()
