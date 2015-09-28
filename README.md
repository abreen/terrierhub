Before getting started, make sure you have:

-   Python 3
-   [Django](https://www.djangoproject.com/download/)

To get a local instance of the app running, run the `setup.sh` script. This
script will create an empty database, run all migrations to set up the tables,
and run the scripts to add the data from the `rawdata/` directory into the
database.

To test the app locally, use the `manage.py` script's `runserver` subcommand.
For help with `manage.py`, invoke it with no arguments.
