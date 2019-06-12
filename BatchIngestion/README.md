# Batch Data Ingestion

## Requirements

This uses the following Python 3 packages:

* `requests`
* `os`
* `boto3`
* `subprocess`

We specifically use `run` from the `subprocess` package, which
requires Python 3.5 or greater.

Note that `boto3` also depends on a properly configured AWS CLI.

The following command line utilities are used:

* `awscli`
* `bzip2` 
* `p7zip-full`
* `xz`
* `zstd`
