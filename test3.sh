#!/usr/bin/env bash
source ~/.bashrc
module load python/gnu/3.6.5
module load spark/2.4.0
rm -r task3_data/
spark-submit --conf spark.pyspark.python=/share/apps/python/3.6.5/bin/python task3_get_data.py