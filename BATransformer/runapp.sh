#!/bin/bash

spark-submit \
    --class App \
    --driver-class-path /usr/share/java/postgresql.jar:/usr/local/spark/lib/hadoop-aws-2.7.1.jar:/usr/local/spark/lib/aws-java-sdk-1.7.4.jar \
    --jars /usr/share/java/postgresql.jar,/usr/local/spark/lib/hadoop-aws-2.7.1.jar,/usr/local/spark/lib/aws-java-sdk-1.7.4.jar \
    target/scala-2.11/business-analysis-transformer_2.11-1.0.jar \
    $1 \
    $2 
