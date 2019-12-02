#!/usr/bin/env bash
source ~/.bashrc
module load python/gnu/3.6.5
module load spark/2.4.0
#spark-submit --num-executors 70 --conf spark.pyspark.python=/share/apps/python/3.6.5/bin/python --executor-memory=6G --driver-memory=4G --conf spark.executor.memoryOverhead=6G  task1.py
spark-submit \
  --num-executors 100 \
  --executor-memory 6G \
  --executor-cores 4 \
  --driver-memory 4G \
  --conf spark.default.parallelism=1000 \
  --conf spark.executor.memoryOverhead=6G \
  --conf spark.storage.memoryFraction=0.5 \
  --conf spark.shuffle.memoryFraction=0.3 \
  task1.py