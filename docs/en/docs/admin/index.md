# initial configuration

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

## Upgrade database to latest version

=== "CLI"
      Command line application

      ```console
      $ flask db upgrade
      ```

      Update modules lists, profiles and permissions

      ```console
      $ flask cli modulesrefresh
      $ flask cli updateprofiles
      $ flask cli updatepermissions
      ```

      Add an addmin

      ```console
      $ flask cli addadmin
      ```

=== "Shell"
      Using interactive shell

      ```console
      $ flask shell
      >>> dir()
      ['Session', 'Tb', '__builtins__', 'app', 'createdb', 'db', 'g', 'registeradmin', 'whatsnext']
      >>>
      ```

      Please use the function whatsnext()

      ```bash
      >>> whatsnext()
      Would you like to create tables? y/n [y]:
      ```

The command line application will guide you through the rest of the setup
process including:

- Create tables.
- Register default profiles.
- Create administrator.
- Update modules permissions by profile.
