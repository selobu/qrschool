# Configuración inicial

Antes de iniciar a trabajar con el api deberá seguir los siguientes pasos:

1. Cree la base de datos "colegio2023" usando mysql o mysqladmin, utilize la codificación utf-8.
2. Use el shell de flask para guiarlo a través de el proceso de instalación.

```bash
$ cd src
```

Entonces active el entorno visual

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

## Actualice la base de datos a la última versión.

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
      Usando la consola

      <div class="termy">

      ```console
      $ flask shell
      $ >>> dir()
      ['Session', 'Tb', '__builtins__', 'app', 'createdb', 'db', 'g', 'registeradmin', 'whatsnext']
      $ >>> whatsnext()
      Would you like to create tables? y/n [y]:
      ```
      </div>

La consola lo guiara a través del proceso de instalción:

- Crear tablas.
- Registrar perfiles por defecto.
- Crear administrador.
- Actualizar permisos por perfil.
