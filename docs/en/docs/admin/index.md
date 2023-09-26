# initial configuration

Before starting work with the api you must do the following steps:

1. Create the database "colegio2023" using mysql or mysqladmin, please use utf-8
   encoding.
2. Use the flask shell to guide you through the rest of setup process

```bash
$ cd src
```

Then activate the virtual environment

<div class="termy">

```bash
$ pipenv shell

(base) <user>:/media/sebastian/datos/Proyectos/qrschool/src$ pipenv shell
Launching subshell in virtual environment...
 . /media/sebastian/datos/Proyectos/qrschool/.venv/bin/activate
(base) <user>:/media/sebastian/datos/Proyectos/qrschool$  . /media/sebastian/datos/Proyectos/qrschool/.venv/bin/activate
(qrschool) (base) <user>:/media/sebastian/datos/Proyectos/qrschool$

$ cd src

```

</div>

## Upgrade database to latest version

===+ "CLI"
      Command line application

      <div class="termy">

      ```console
      $ flask db upgrade
      INFO  [alembic.runtime.migration] Context impl MySQLImpl.
      INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
      ```

      </div>

      Update modules lists, profiles and permissions

      <div class="termy">

      ```console
      $ flask cli modulesrefresh
      $ flask cli updateprofiles
      $ flask cli updatepermissions
      ```

      </div>

      Add an addmin

      <div class="termy">

      ```console
      $ flask cli addadmin
      email: <mymail>@mail.com
      firstname: Sebastian
      lastname: Lopez
      número de identificación: ...
      ```

      </div>

=== "Shell"
      Using the console

      <div class="termy">

      ```console
      $ flask shell
      $ >>> dir()
      ['Session', 'Tb', '__builtins__', 'app', 'createdb', 'db', 'g', 'registeradmin', 'whatsnext']
      $ >>> whatsnext()
      Would you like to create tables? y/n [y]:
      ```
      </div>

The command line application will guide you through the rest of the setup
process including:

- Create tables.
- Register default profiles.
- Create administrator.
- Update modules permissions by profile.
