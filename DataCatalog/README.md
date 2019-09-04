# Data Catalog

The purpose of this app is to build the components of the data
catalog.  For each of our three data sources, we want to build a data
dictionary and basic statistics.

This is accomplished by using a Spark cluster to examine the text files
in the S3 bucket created by the `BatchIngestion` process.

## Running the Spark Job

All the relevant code is contained in the `/src/main/scala/`
folder, but running the app can be with the `runapp.sh` script.

First, the source code should be packaged.  This is accomplished using
the Scala SBT with the command
```
sbt package
```

The shell script `runapp.sh` then can be used to submit the Spark job. 
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
