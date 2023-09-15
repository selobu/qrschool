from flask import current_app as app
from flask import redirect, render_template, url_for, request, send_from_directory
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user
from sqlalchemy import select
from wtforms import EmailField, StringField, BooleanField
from wtforms.validators import DataRequired, Length
from os.path import join as pathjoin


def init_app(app):
    pass


class RegisterForm(FlaskForm):
    correo = EmailField(
        validators=[DataRequired("Ingrese el correo"), Length(min=8, max=40)],
    )
    password = StringField(validators=[DataRequired("Ingrese al contraseña")])
    recordarme = BooleanField("Recordarme")


@app.route("/", methods=["GET"])
def index():
    """This endpoint is to auth the administrator console only"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """This endpoint is to auth the administrator console only"""
    form = RegisterForm()
    if form.validate_on_submit():
        next = request.args.get("next")
        # verificar que las credenciales sean válidas
        with app.Session() as session:
            smts = select(app.Tb.User).filter(app.Tb.User.correo == form.correo.data)
            res = session.execute(smts).one()
            user = res[0]
            if not user.validatepassword(form.password.data):
                return redirect("#")
            # storing data
            login_user(user, remember=form.recordarme.data)
        return redirect(next or url_for("admin.index"))
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """This endpoint is to logout the administrator"""
    logout_user()
    return redirect(url_for("login"))


print("ROOT PATH")
print(app.root_path)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        pathjoin(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
