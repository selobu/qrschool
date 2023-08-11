FROM python:3.11.2
LABEL "maintainer"="Sebastian López Buritica <selobu at gamil dot com>"
RUN  pip install --upgrade pip
RUN  pip install pydantic[email] python-multipart
RUN  pip install sqlalchemy
RUN  pip install sqlmodel