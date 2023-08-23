# coding:utf-8
# needs to be called outside this cicle and just run once.
from flask import current_app as app
from app.toolsapk import map_name_to_shell
from app.toolsapk import Tb, gethash
import getpass


@map_name_to_shell
def registeradmin():
    print("* Admin register")
    name = input("name: ")
    lastname = input("last name: ")
    numeroidentificacion = input("Id number: ")
    fechaNacimiento = input("Fecha nacimiento YYYY-MM-DD: ")
    rh = input("rh: ")
    direccion = input("direccion: ")
    telefono = input("telefono: ")
    email = input("Email: ")

    while True:
        password = getpass.getpass(prompt="Password: ", stream=None)
        password2 = getpass.getpass(prompt="confirm password: ", stream=None)
        if password != password2:
            print("Password confirm must be the same")
            return
        else:
            break
    with app.Session() as session:
        user = Tb.User.register(
            is_active=True,
            nombres=name,
            apellidos=lastname,
            perfil_nombre="administrador",
            correo=email,
            fechaNacimiento=fechaNacimiento,
            rh=rh,
            direccion=direccion,
            telefono=telefono,
            numeroidentificacion=numeroidentificacion,
        )
        session.add(user)
        session.commit()
        userid = user.id

    with app.Session() as session:
        # se registra la contraseña del usuario
        password = Tb.Auth.register(usuario_id=userid, hash=gethash(password))
        session.add(password)
        session.commit()
        print("Usuario administrador creado exitosamente")
