# BATransformer

The purpose of this package is to transform the raw data and load it
into the database that will serve as our data warehouse for social
media comments.  The source code is entirely in `src/main/scala`, but
to use the app it is only necessary to use the `runapp.sh` script
with a few command line options.

The syntax for using the script is
```
./runapp.sh <datasource>
```
The three valid choices for `<datasource>` are `reddit`, `stackexchange`, 
and `hackernews`.
