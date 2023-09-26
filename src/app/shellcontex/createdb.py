# coding:utf-8
# needs to be called outside this cicle and just run once.
from app.toolsapk import Base
from flask import current_app as app
from app.toolsapk import map_name_to_shell


@map_name_to_shell
def createdb():
    Base.metadata.create_all(app.engine)
