from flask import current_app as app
from flask import redirect, render_template, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


def init_app(app):
    pass


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])


@app.route("/", methods=["GET"])
def index():
    """This endpoint is to auth the administrator console only"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """This endpoint is to auth the administrator console only"""
    form = PhotoForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", form=form)
