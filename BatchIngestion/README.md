# Batch Data Ingestion

## Purpose

The python scripts in this folder are used to download and unpack
source files for information on comments from Reddit, Stack Exchange,
and Hacker News.  The text files are stored in an S3 bucket which must
be configured using AWS CLI.

## Requirements

This uses the following Python 3 packages:

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
* `wget`
* `zstd`
