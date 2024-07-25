from app import create_app
from app.shellcontex.registeradmin import regadmin

app = create_app()

with app.app_context():
    regadmin(
        name="Sebastian",
        lastname="Lopez",
        numeroidentificacion=75100175,
        fechaNacimiento="1981-12-17",
        rh="O+",
        direccion="Calle siemppre viva",
        telefono="3196032071",
        email="selobu@gmail.com",
        password="123456789",
    )
