#!/usr/bin/env bash
source ~/.bashrc
module load python/gnu/3.6.5
module load spark/2.4.0
rm -r task2_data/
#spark-submit task1.py /user/hm74/NYCOpenData/datasets.tsv
spark-submit --conf spark.pyspark.python=/share/apps/python/3.6.5/bin/python task2.py
