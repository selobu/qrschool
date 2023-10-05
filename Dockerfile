FROM python:3.11.2
LABEL "maintainer"="Sebastian López Buritica <selobu at gamil dot com>"
WORKDIR /var/wwww

COPY ./pyproject.toml  ./pyproject.toml
COPY ./src/gunicorn_config.py  ./gunicorn_config.py
COPY ./src ./

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# reading port from gobal variable
EXPOSE ${SERVING_PORT}
CMD ["gunicorn","--config", "gunicorn_config.py", "main:app"]
