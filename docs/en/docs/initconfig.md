## initial configuration

Before starting work with the api you must do the following steps:

1. Create the database "colegio2023" using mysql or mysqladmin, please use utf-8
   encoding.
2. Use the flask shell to guide you through the rest of setup process

```bash
$ cd src
```

Then activate the virtual environment

```bash
$ pipenv shell
```

```bash
$ flask shell
>>> dir()
['Session', 'Tb', '__builtins__', 'app', 'createdb', 'db', 'g', 'registeradmin', 'whatsnext']
>>>
```

Please use the function whatsnext()

```python
>>> whatsnext()
Would you like to create tables? y/n [n]:
```

The command line application will guide you through the rest of the setup process including:

* Create tables.
* Register default profiles.
* Create administrator.
* Update modules permissions by profile.
