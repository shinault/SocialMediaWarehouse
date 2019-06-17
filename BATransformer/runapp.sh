#!/bin/bash

spark-submit \
    --class App \
    target/scala-2.11/business-analysis-transformer_2.11-1.0.jar \
    $1 \
    $2 
