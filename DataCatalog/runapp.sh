#!/bin/bash

DCPATH=/usr/share/java/postgresql.jar
DCPATH=$DCPATH:/usr/local/spark/lib/hadoop-aws-2.7.1.jar
DCPATH=$DCPATH:/usr/local/spark/lib/aws-java-sdk-1.7.4.jar
DCPATH=$DCPATH:/usr/local/spark/lib/spark-xml_2.11-0.5.0.jar

JARS=/usr/share/java/postgresql.jar
JARS=$JARS,/usr/local/spark/lib/hadoop-aws-2.7.1.jar
JARS=$JARS,/usr/local/spark/lib/aws-java-sdk-1.7.4.jar
JARS=$JARS,/usr/local/spark/lib/spark-xml_2.11-0.5.0.jar

spark-submit \
    --class App \
    --driver-class-path $DCPATH \
    --jars $JARS \
    --master $SPARK_MASTER_PATH \
    target/scala-2.11/data-catalog-builder_2.11-1.0.jar \
    $1 \
    $2 
    
