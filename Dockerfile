FROM python:3.11.2
LABEL "maintainer"="Sebastian López Buritica <selobu at gamil dot com>"
##COPY ./requirements.txt /var/www/requirements.txt

WORKDIR /var/wwww

RUN pip3 install --upgrade pip
RUN pip3 install poetry
COPY ./pyproject.toml  ./pyproject.toml
COPY ./src/gunicorn_config.py  ./gunicorn_config.py
RUN poetry config virtualenvs.create false
RUN poetry install
## RUN pip3 install -r /var/www/requirements.txt
## COPY ./src/gunicorn_config.py  ./home/gunicorn_config.py
COPY ./src ./
EXPOSE 8081
CMD ["gunicorn","--config", "gunicorn_config.py", "main:app"]
