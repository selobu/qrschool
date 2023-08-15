---

QRSchool is a rest-api built on top of Python 3.8 and Flask.

The key features are:

- **Secure**: based onb JSON web tokens.
- **Intuitive**: The api is extended explained.
- **Easy**: as easy as posible, its modular to be deploy in different platforms
  such as amazon, google, pythonanywhere asn so on.
- **Modular**: Is simple to create additional modules base on needs.
- **Database-ready**: It's predonfigured to with mysql but can be moddified to
  be connected to a wide range of databases

## Sponsors

<!-- sponsors -->

{% if sponsors %} {% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%} {%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %} {% endif %}

<!-- /sponsors -->

<a href="https://gestionhseq.com/#sponsors" class="external-link" target="_blank">Other
sponsors</a>

## Opinions

## Requirements

Python 3.8+

Some dependecies:

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

## Installation

<div class="termy">

```console
$ ......

---> 100%
```

</div>

You will also need a WSGI server, for production such as
<a href="https://www.gunicorn.org" class="external-link" target="_blank">Gunicorn</a>

<div class="termy">

```console
$ pip install git+https://github.com/benoitc/gunicorn.git

---> 100%
```

</div>
