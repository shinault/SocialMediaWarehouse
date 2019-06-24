# Data Catalog

The purpose of this app is to build the components of the data
catalog.  For each of our three data sources, we want to build a data
dictionary and basic statistics.

All the relevant code is contained in the `/src/main/scala/`
folder, but running the app can be with the `runapp.sh` script.

The syntax for running the app is simply
```
./runapp.sh <command> <datasource>
```
The two valid `<command>` choices are `dictionary` and `stats`.
The three valid choices for `<datasource>` are `reddit`, `stackexchange`,
and `hackernews`.

All the code is written to run a Spark cluster with authorized access
to the private S3 bucket containing the data, and write the tables to
a Postgres database that has been specified in environmental variables.
