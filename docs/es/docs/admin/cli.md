# Cli

A command-line interface [CLI](https://en.wikipedia.org/wiki/Command-line_interface)
is a means of interacting with a computer program by inputting lines of text called command-lines.

We create a command line application to allow the system administration easily setup the
environment. The following command are designed to specific tasks in the backend.

There are two main commands wich are *db* and *cli*

## db

This command is inherith from flask migrate so please be carfull to prevent data loose.

List all commands available

???+ warning "Don't forget to"

    Remember to run de following commands in src or equivalent folder where app resides, and
    activate the virtual environment.

<div class="termy">
```console
$ flask db --help

Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  An application to load must be given with the '--app' option, 'FLASK_APP'
  environment variable, or with a 'wsgi.py' or 'app.py' file in the current
  directory.

Options:
  -e, --env-file FILE   Load environment variables from this file. python-
                        dotenv must be installed.
  -A, --app IMPORT      The Flask application or factory function to load, in
                        the form 'module:name'. Module can be a dotted import
                        or file path. Name is not required if it is 'app',
                        'application', 'create_app', or 'make_app', and can be
                        'name(args)' to pass arguments.
  --debug / --no-debug  Set debug mode.
  --version             Show the Flask version.
  --help                Show this message and exit.

Commands:
  cli     Command line system administration
  db      Perform database migrations.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```

</div>

To check the db options available

<div class="termy">
```console
$ flask db --help

Usage: flask db [OPTIONS] COMMAND [ARGS]...

  Perform database migrations.

Options:
  --help  Show this message and exit.

Commands:
  branches        Show current branch points
  check           Check if there are any new operations to migrate
  current         Display the current revision for each database.
  downgrade       Revert to a previous version
  edit            Edit a revision file
  heads           Show current available heads in the script directory
  history         List changeset scripts in chronological order.
  init            Creates a new migration repository.
  list-templates  List available templates.
  merge           Merge two revisions together, creating a new revision file
  migrate         Autogenerate a new revision file (Alias for 'revision...
  revision        Create a new revision file.
  show            Show the revision denoted by the given symbol.
  stamp           'stamp' the revision table with the given revision;...
  upgrade         Upgrade to a later version
```
</div>

If you want to check an specific command you can request help using the command --help as a command option

<div class="termy">
```console
$ flask db upgrade --help

Usage: flask db upgrade [OPTIONS] [REVISION]

  Upgrade to a later version

Options:
  -d, --directory TEXT  Migration script directory (default is "migrations")
  --sql                 Don't emit SQL to database - dump to standard output
                        instead
  --tag TEXT            Arbitrary "tag" name - can be used by custom env.py
                        scripts
  -x, --x-arg TEXT      Additional arguments consumed by custom env.py scripts
  --help                Show this message and exit.
```

</div>

## cli

This commands group were created to configure the database and profiles

<div class="termy">
```console
$ flask cli --help

Usage: flask cli [OPTIONS] COMMAND [ARGS]...

  Command line system administration

Options:
  --help  Show this message and exit.

Commands:
  addadmin           Create an administrator given the email
  admincount         Count the number of active administrators
  createdb           Create tables and relationships
  modulesrefresh     Refresh modules
  removeadmin        Removes user as administrator
  updatepermissions  Permision refresh by profile
  updateprofiles     Update profiles
```

</div>

If you want to check an specific command you can request help using the command --help as a command option

<div class="termy">
```console
  $ flask cli addadmin --help

  Usage: flask cli addadmin [OPTIONS]

    Create an administrator given the email

  Options:
    --email TEXT
    --name TEXT
    --lastname TEXT
    --id INTEGER
    --date TEXT
    --rh TEXT
    --direccion TEXT
    --telefono TEXT
    --password TEXT
    --help            Show this message and exit.
```

</div>
