__all__ = ["getviews"]
from flask_admin.contrib.sqla import ModelView
from app.toolsapk import Tb
from flask import current_app as app


def getviews() -> list:
    views = list()

    views.append(ModelView(Tb.User, app.Session()))  # type: ignore
    return views
