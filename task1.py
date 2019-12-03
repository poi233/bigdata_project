# -*- coding: UTF-8 -*-
import json
import os
import re

from dateutil.parser import *
from pyspark.sql import SparkSession

MIN_SIZE = 500000

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def get_type(x):
    if is_null(x):
        return "NONE"
    int_pattern = re.compile(r'^\d+$')
    float_pattern = re.compile(r'^\d+\.\d*$')
    if len(x) >= 6:
        try:
            parse(x)
            return "DATE/TIME"
        except:
            pass
    if int_pattern.match(x.replace(",", "")):
        try:
            int(x.replace(",", ""))
            return "INTEGER"
        except:
            pass
    if float_pattern.match(x.replace(",", "")):
        try:
            float(x.replace(",", ""))
            return "REAL"
        except:
            pass
    return "TEXT"


def is_null(x):
    return x is None or x == ""


def not_null(x):
    return x is not None and x != ""


def combine_types(a, b):
    if a[0] == "NONE":
        return b
    elif b[0] == "NONE":
        return a
    elif a[0] == "INTEGER" and b[0] == "REAL":
        return b
    elif b[0] == "INTEGER" and a[0] == "REAL":
        return a
    elif a[1] > b[1]:
        return a
    else:
        return b


def profile(dataset):
    print("%s start processing................................." % dataset)
    output = dict()
    output["dataset_name"] = dataset
    output["columns"] = []
    output["key_column_candidates"] = []
    dataset_df = spark.read.format('csv').options(header='true', inferschema='true', sep='\t').load(data_dir + dataset + ".tsv.gz")
    print("%s data load ok" % dataset)
    df_count = dataset_df.count()
    if df_count == 0:
        print("%s has no data" % dataset)
        return
    if df_count > MIN_SIZE:
        print("%s is a large dataset skip now" % dataset)
        return
    columns = dataset_df.columns
    for column_name in columns:
        valid_column_name = column_name.replace(".", "").replace("`", "")
        dataset_df = dataset_df.withColumnRenamed(column_name, valid_column_name)
        print("start column %s" % column_name)
        # get col
        col_rdd = dataset_df.select(valid_column_name.replace(".", "")).rdd.map(lambda x: str(x[0])).cache()
        # get col type
        col_type = col_rdd.map(lambda x: (get_type(x), 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .reduce(combine_types)[0]
        print("%s type is %s" % (column_name, col_type))
        # get col stat
        number_non_empty_cells = col_rdd.filter(not_null).count()
        number_empty_cells = col_rdd.filter(is_null).count()
        number_distinct_values = col_rdd.distinct().count()
        frequent_values = col_rdd.map(lambda x: (x, 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .sortBy(lambda x: -x[1]) \
            .map(lambda x: x[0]) \
            .take(5)
        # get col stat according to type
        data_types = dict()
        data_types["type"] = col_type
        data_types["count"] = number_non_empty_cells + number_empty_cells
        if col_type == "REAL":
            col_rdd = col_rdd.filter(lambda x: get_type(x) == "REAL" or get_type(x) == "INTEGER").map(
                lambda x: float(x.replace(",", ""))).cache()
            min_value = col_rdd.min()
            max_value = col_rdd.max()
            data_types["min_value"] = min_value if min_value is not None else None
            data_types["max_value"] = max_value if max_value is not None else None
            data_types["mean"] = col_rdd.mean()
            data_types["stddev"] = col_rdd.stdev()
        elif col_type == "INTEGER":
            col_rdd = col_rdd.filter(lambda x: get_type(x) == "INTEGER").map(lambda x: int(x.replace(",", ""))).cache()
            min_value = col_rdd.min()
            max_value = col_rdd.max()
            data_types["min_value"] = min_value if min_value is not None else None
            data_types["max_value"] = max_value if max_value is not None else None
            data_types["mean"] = col_rdd.mean()
            data_types["stddev"] = col_rdd.stdev()
        elif col_type == "TEXT":
            col_rdd = col_rdd.filter(lambda x: x is not None).map(lambda x: x.encode("utf-8")).cache()
            data_types["shortest_values"] = col_rdd.distinct() \
                .takeOrdered(5, key=lambda x: (len(x), x))
            data_types["longest_values"] = col_rdd.distinct() \
                .takeOrdered(5, key=lambda x: (-len(x), x))
            total_length, count = col_rdd.map(lambda x: (len(x), 1)) \
                .reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]))
            data_types["average_length"] = float(total_length) / float(count) if count > 0 else 0
        elif col_type == "DATE/TIME":
            col_rdd = col_rdd.filter(lambda x: get_type(x) == "DATE/TIME").map(
                lambda x: (str(x), parse(str(x)))).cache()
            min_value = col_rdd.min(lambda x: x[1])
            max_value = col_rdd.max(lambda x: x[1])
            data_types["min_value"] = min_value[0] if min_value is not None else None
            data_types["max_value"] = max_value[0] if max_value is not None else None
        else:
            data_types["type"] = "TEXT"
            data_types["count"] = number_non_empty_cells + number_empty_cells
            data_types["shortest_values"] = []
            data_types["longest_values"] = []
            data_types["average_length"] = []
        # identify candidate for keys
        if col_type != "DATE/TIME" and number_distinct_values == number_empty_cells + number_non_empty_cells:
            output["key_column_candidates"].append(column_name)
        # save data
        column = dict()
        column["column_name"] = column_name
        column["number_non_empty_cells"] = number_non_empty_cells
        column["number_empty_cells"] = number_empty_cells
        column["number_distinct_values"] = number_distinct_values
        column["frequent_values"] = frequent_values
        column["data_types"] = data_types
        output["columns"].append(column)
        print("column %s ok" % column_name)
    # save to json file
    with open("./task1_data/%s.json" % dataset, 'w') as fp:
        json.dump(output, fp, cls=MyEncoder)
    print("%s processed OK" % dataset)


if __name__ == "__main__":
    # init
    spark = SparkSession \
        .builder \
        .appName("bigdata_project") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    # get file and dir
    file = "/user/hm74/NYCOpenData/datasets.tsv"
    data_dir = file[:file.rfind("/") + 1]
    data_sets = spark.read.format('csv').options(header='true', inferschema='true', sep='\t').load(file).rdd.map(
        lambda x: x[0]).collect()
    # create result dir
    mkdir("./task1_data")
    # run profile for each dataset
    offset = int(len(data_sets) / 3)
    my_dir = '/home/yp1207/project_pycharm/task1_data/'
    big_datasets = []
    has_not_done = True
    while has_not_done:
        not_done = 0
        for i in range(offset + 1):
            if data_sets[i + offset] in big_datasets:
                continue
            if i + offset >= len(data_sets):
                break
            if not os.path.exists(my_dir + data_sets[i + offset] + ".json"):
                not_done += 1
                profile(data_sets[i + offset])
            else:
                print("%s already processed" % data_sets[i + offset])
        if not_done == 0:
            has_not_done = False
        MIN_SIZE += 500000

