from flask import current_app as app
from flask import request


def init_app(app):
    pass


@app.route("/login", methods=["GET", "POST"])
def login():
    """This endpoint is to auth the administrator console only"""
    if request.method == "POST":
        return "loging"

    return "<p>Login!</p>"
