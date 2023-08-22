# coding:utf-8
__all__ = ["whatsnext"]

from app.toolsapk import map_name_to_shell
from sqlalchemy import select, func
from app.toolsapk import shell_decorated
from app.modules.User.model import PerfilSchool
import app.modules as _modules
from flask import current_app as app
from pathlib import Path


def _listsubmodules(filepath):
    modulespath = Path(filepath).parent
    modules = list()
    for element in list(modulespath.glob("*")):
        if not element.is_dir():
            continue
        dir(element)
        modules.append(element.name)
    return [m for m in modules if not m.startswith("_")]


@map_name_to_shell
def whatsnext():
    # check if tables exists
    table_created = input("Would you like to create tables? y/n [n]: ")
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
    update_profile = "n"
    if len(missing) > 0:
        update_profile = input("Desea actualizar los perfiles? y/n [n]: ")
    else:
        print("all profiles are registered!")
    if update_profile in ("y", "yes"):
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

    agregaradmin = "n"
    if cantidadadministradores == 0:
        agregaradmin = input(
            "No se detectaron usuarios administadores, desea agregar uno? y/n [n]: "
        )
    if agregaradmin in ("y", "yes"):
        shell_decorated["registeradmin"]()
    # current modules
    available_modules = _listsubmodules(_modules.__file__)
    with app.Session() as session:
        # smts = select(app.Tb.Perfil.nombreperfil)
        # perfiles = [p[0].value for p in session.execute(smts).all()]
        smts = select(app.Tb.Module.modulename)
        modulenames = [p[0] for p in session.execute(smts).all()]
        missingmodules = [u for u in available_modules if u not in modulenames]
    update_moduleslist = "n"
    if len(missingmodules) > 0:
        update_moduleslist = input("Desaa actualizar los modulos? y/n [n]: ")
    else:
        print("El listado de modulos está actualizado")
    if update_moduleslist.lower() in ("y", "yes"):
        with app.Session() as session:
            session.add_all(
                [app.Tb.Module.register(modulename=name) for name in missingmodules]
            )
            session.commit()
        print(f"Se actualizaron con exito los módulos {missingmodules}")
        print("es necesario actualizar el listado de permisos")
    # actualizar los modulos
    with app.Session() as session:
        smts = select(app.Tb.Perfil.nombreperfil)
        perfiles = [r[0].value for r in session.execute(smts).all()]
        smts = select(app.Tb.Module.modulename)
        modulenames = [p[0] for p in session.execute(smts).all()]
        lista = list()
        for modulename in modulenames:
            for permision in perfiles:
                lista.append((permision, modulename))
        smts = select(
            app.Tb.PerfilModuloLnk.perfil_id, app.Tb.PerfilModuloLnk.modulo_id
        )
        registrados = session.execute(smts).all()
        missing = [f for f in lista if f not in registrados]
    if len(missing) > 0:
        print(f"missing {missing}")
        if input("Desea actualizar el listado de permisos? y/n [y]").lower() in (
            "y",
            "yes",
            "",
        ):
            with app.Session() as session:
                session.add_all(
                    [
                        app.Tb.PerfilModuloLnk.register(
                            perfil_id=perfil, modulo_id=module
                        )
                        for (perfil, module) in missing
                    ]
                )
                session.commit()
            print("Actualizado")
