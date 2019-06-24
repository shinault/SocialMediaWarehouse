# SayWhat

A warehouse for social media comments.


## Overview

Build a data warehouse to serve as a single source for information
from many social media sites.


## Installation

There are at a minimum two computing systems that must be set up to
use the code in this project: a Spark cluster and a (Postgres)
database.

Instructions for installation and dependencies for a Spark cluster are
found in `SparkCluster.org`.  There is a little more flexibility in 
database choice, if the source code in this repo is slightly modfied.

There are four logically separate components to this project, maintained in
separate folders.  Details about the usage and dependencies for each component
are contained in their respective folders.

1. Loading data into S3: `BatchIngestion` folder.
2. Basic analysis on data to build a data catalog for raw data:
   `DataCatalog` folder.
2. Filter and join raw data to build a data warehouse: `BATransformer`
   folder.
4. Building a dashboard off of the warehouse: `Dashboard` folder.


## Architecture

1. Raw data storage: Amazon S3.
2. Processing framework: Apache Spark
3. Datastore: PostgreSQL
4. Dashboard: Flask

## Data Source

* Stack Exchange Posts and Answers: XML in numerous files
* Hacker News Comments: JSON comments and XML metadata, in a few files
* Reddit Comments: JSON comments across many files


## Engineering Challenges

