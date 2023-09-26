# /usr/bin python3
# coding:utf-8
import click
from flask.cli import AppGroup
from app.shellcontex.createdb import createdb as cli_createdb
from app.shellcontex.registeradmin import regadmin
from app.toolsapk import Tb
from sqlalchemy import select
import app.modules as _modules
from app.modules.User.model import PerfilSchool
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


def init_app(app):
    cli = AppGroup("cli", help="Command line system administration")

    @cli.command(help="Create tables and relationships")
    def createdb():
        click.echo("Creating tables and relationships")
        cli_createdb()

    @cli.command(help="Create an administrator given the email")
    @click.option("--email", type=str, prompt="email")
    @click.option("--name", type=str, prompt="firstname")
    @click.option("--lastname", type=str, prompt="lastname")
    @click.option("--id", type=int, prompt="número de identificación")
    @click.option("--date", type=str, prompt="Fecha nacimiento: YYYY-MM-DD")
    @click.option("--rh", type=str, prompt="Factor RH")
    @click.option("--direccion", type=str, prompt="direccion")
    @click.option("--telefono", type=str, prompt="telefono")
    @click.option(
        "--password", type=str, prompt=True, hide_input=True, confirmation_prompt=True
    )
    def addadmin(email, name, lastname, id, date, rh, direccion, telefono, password):
        click.echo("Creating the administrator")
        regadmin(name, lastname, id, date, rh, direccion, telefono, email, password)

    @cli.command(help="Removes user as administrator")
    @click.option("--email", prompt="email")
    def removeadmin(email):
        click.echo(f"Removing admin profile {email}")
        with app.Session() as session:
            res = select(Tb.User).join(Tb.Perfil.user).filter(Tb.User.correo == email)
            user = session.execute(res).one()[0]
            print(user)
            user.perfil_nombre = "SIN"
            session.add(user)
            session.commit()

    @cli.command(help="Update profiles")
    def updateprofiles():
        click.echo("Updating profiles")
        missing = []
        with app.Session() as session:
            res = select(app.Tb.Perfil.nombreperfil).limit(20)
            registerd = [r[0].value for r in session.execute(res).all()]
            print(f"registerd {registerd}")
            missing = [
                perfil.value
                for perfil in list(PerfilSchool)
                if perfil.value not in registerd
            ]
        if len(missing) == 0:
            click.echo("Nada para actualizar")
            return
        with app.Session() as session:
            session.add_all(
                [app.Tb.Perfil.register(nombreperfil=miss) for miss in missing]
            )
            session.commit()

    @cli.command(help="Count the number of active administrators")
    def admincount():
        click.echo("Showing system administrators")
        with app.Session() as session:
            res = (
                select(Tb.User.nombres, Tb.User.correo)
                .join(Tb.User.perfil)
                .filter(Tb.Perfil.nombreperfil == "ADMINISTRADOR")
            )

            r = session.execute(res).all()
            click.echo(f"Total: {len(r)}")
            for pos, line in enumerate(r, start=1):
                click.echo(f"{pos}- {line[0]} {line[1]}")

    @cli.command(help="Refresh modules")
    def modulesrefresh():
        click.echo("Updating modules")
        # current modules
        available_modules = _listsubmodules(_modules.__file__)
        with app.Session() as session:
            # smts = select(app.Tb.Perfil.nombreperfil)
            # perfiles = [p[0].value for p in session.execute(smts).all()]
            smts = select(app.Tb.Module.modulename)
            modulenames = [p[0] for p in session.execute(smts).all()]
            missingmodules = [u for u in available_modules if u not in modulenames]
        update_moduleslist = "n"
        if len(missingmodules) == 0:
            click.echo("El listado de modulos está actualizado")
            return
        if update_moduleslist.lower() in ("y", "yes"):
            with app.Session() as session:
                session.add_all(
                    [app.Tb.Module.register(modulename=name) for name in missingmodules]
                )
                session.commit()

    @cli.command(help="Permision refresh by profile")
    def updatepermissions():
        click.echo("Updating profile permisions")
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
        with app.Session() as session:
            session.add_all(
                [
                    app.Tb.PerfilModuloLnk.register(perfil_id=perfil, modulo_id=module)
                    for (perfil, module) in missing
                ]
            )
            session.commit()

    app.cli.add_command(cli)
