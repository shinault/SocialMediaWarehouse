# BATransformer

The purpose of this package is to transform the raw data and load it
into the database that will serve as our data warehouse for social
media comments.

Comments are ingested from the text files in an S3 bucket, common
fields are selected, and the resulting Spark DataFrames are stored in
a PostgresQL database.


## Running the Spark Job

The source code is entirely in `src/main/scala`, but to use the app it
is only necessary to use the `runapp.sh` script with a few command
line options.

The syntax for using the script is
```
./runapp.sh <datasource>
```
The three valid choices for `<datasource>` are `reddit`, `stackexchange`, 
and `hackernews`.
