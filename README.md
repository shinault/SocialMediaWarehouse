# Social Media Warehouse

## Business Problem

There are many opportunities to explore social media comments!

* Business analysts want to know how many mentions there are of a new
  product.
* Data scientists can refine the business analysts’ problem into
  sentiment analysis across websites.
* Data scientists want to identify unique users with multiple accounts
  across websites for targeted marketing.  
  
**The issue**: analysts and data scientists should focus on what to do
with the data, not on how to collect it from the numerous sources.

## Idea

Build a data warehouse to serve as a single source for information
from many social media sites.

## Data Source

Stack Exchange Posts and Answers: XML in numerous files

14 Million Hacker News Comments: JSON comments and XML metadata, in a few files

Reddit Comments: JSON comments across many files

## MVP

A data warehouse that

* collects from at least two disparate data sources.
* is easy to build the business analysts’ dashboard on top of.  It can
  show basic count data for topics in a time window as part of a demo.


## Stretch Goals

* Add additional data sources such as Disqus comments on a specific
  blog or website.
* Make the data ingestion actually live streaming rather than only
  simulated.
* Determine a way to make the ingestion robust to (mild) format
  changes.
* Build the sentiment analysis dashboard (too data science-y?)


## Engineering Challenge

* Determining an appropriate schema to store data with slightly
  different formats, with the flexibility to be useful for at least
  the three identified use cases.
* Ingesting distinct data sources into a single store.
* Designing a clean API to query the data.


## Tech Stack

1. Store files in S3.
2. Ingestion framework: MSK
3. Datastore: RDBMS
4. Dashboard: Play (is Tableau feasible?)

