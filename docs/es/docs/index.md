# Indice

QRSchool es una aplicación hecha con Python +3.9, Flask y Vuejs.

Características principales:

- **Seguro**: Se basa en JSON web tokens.
- **Intuitivo**: El api esta explicado de forma detallado.
- **Fácil**: tan fácil como sea posible, es modular para ser desplegado en dferentes plataformas como amazon, gpc, pythonanywhere entre otros.
- **Modular**: Fácil de crear módulos nuevos según se necesite.
- **Base de datos- listo**: pre-configurado con mysql pero puede ser modificado para
conectarse con otras bases de datos relacionales

## Patrocinadores

<!-- sponsors -->

{% if sponsors %} {% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%} {%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %} {% endif %}

<!-- /sponsors -->

<a href="https://gestionhseq.com/#sponsors" class="external-link" target="_blank">Other
sponsors</a>

## Opiniones

## Requerimientos

Python 3.9+

Algunas dependencias:

- <a href="https://flask.palletsprojects.com/en/2.3.x/" class="external-link" target="_blank">Flask</a>
  for the web parts.
- <a href="https://flask-cors.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-Cors</a>
  for the data parts.
- <a href="https://flask-jwt-extended.readthedocs.io/en/stable/" class="external-link" target="_blank">Flask-JWT-Extended</a>
  for the data parts.
- <a href="https://flask-restx.readthedocs.io/en/latest/" class="external-link" target="_blank">Flask-restx</a>
  for the data parts.
- <a href="https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/#" class="external-link" target="_blank">Flask-SQLAlchemy</a>
  for the data parts.
- <a href="https://docs.sqlalchemy.org/en/20/" class="external-link" target="_blank">SQLAlchemy</a>
  for the data parts.
- <a href="https://pymysql.readthedocs.io/en/latest/" class="external-link" target="_blank">PyMySQL</a>
  for the data parts.
- <a href="https://github.com/jpadilla/pyjwt" class="external-link" target="_blank">PyJWT</a>
  for the data parts.

## Installación

Puedes instalar docker en tu computador <a href="https://docs.docker.com/compose/" class="external-link" target="_blank">Docker compose</a>

<div class="termy">

```console
$ docker-compose restart worker

---> 100%
```

</div>

Tambien necesitas in servicdor WSGI para un entorno de producción:
<a href="https://www.gunicorn.org" class="external-link" target="_blank">Gunicorn</a>

<div class="termy">

```console
$ pip install git+https://github.com/benoitc/gunicorn.git

---> 100%
```

El software atualmente se encuentra hospedado en <a href="https://www.pythonanywhere.com" class="external-link" target="_blank">PythonAnywhere</a> así que no
es necesario realizar una configuración adicional para ejecutarlo.
</div>
