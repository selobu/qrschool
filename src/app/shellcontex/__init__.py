# coding:utf-8
from app.toolsapk import Tb
from app.toolsapk import shell_decorated
from app.toolsapk import import_submodules

__all__ = import_submodules(__package__)


def init_app(app):
    def make_shell_context():
        return dict(db=app.db, Tb=Tb, Session=app.Session, **shell_decorated)

    app.shell_context_processor(make_shell_context)
