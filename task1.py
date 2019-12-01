# -*- coding: UTF-8 -*-
import json
import os
import re
import time

from pyspark import SparkContext


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
    if int_pattern.match(x.replace(",", "")):
        return "INTEGER"
    if float_pattern.match(x.replace(",", "")):
        return "REAL"
    try:
        # datefinder.find_dates()
        date = reorganize(x)
        time.strptime(date, "%Y-%m-%d")
        return "DATE"
    except ValueError:
        return "TEXT"


# e.g. 2008-05-29T00:00:00
def reorganize(x):
    if "T" in x:
        x = x.split("T")[0]
    for c in x:
        if not c.isdigit():
            x.replace(c, "-")
    return x


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
    output = dict()
    output["dataset_name"] = dataset
    output["columns"] = []
    dataset_rdd = sc.textFile(data_dir + dataset + ".tsv.gz").map(lambda x: x.split("\t"))
    header = dataset_rdd.first()
    dataset_rdd = dataset_rdd.filter(lambda line: line[0] != header[0])
    for i in range(len(header)):
        # get col
        col_rdd = dataset_rdd.map(lambda x: x[i] if i < len(x) else None).cache()
        # get col type
        col_type = col_rdd.map(lambda x: (get_type(x), 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .reduce(combine_types)[0]
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
            col_rdd = col_rdd.filter(lambda x: get_type(x) == "REAL").map(lambda x: float(x.replace(",", ""))).cache()
            min_value = col_rdd.sortBy(lambda x: x).take(1)
            max_value = col_rdd.top(1)
            data_types["min_value"] = min_value[0] if len(min_value) > 0 else None
            data_types["max_value"] = max_value[0] if len(max_value) > 0 else None
            data_types["mean"] = col_rdd.mean()
            data_types["stddev"] = col_rdd.stdev()
        elif col_type == "INTEGER":
            col_rdd = col_rdd.filter(lambda x: get_type(x) == "INTEGER").map(lambda x: int(x.replace(",", ""))).cache()
            min_value = col_rdd.sortBy(lambda x: x).take(1)
            max_value = col_rdd.top(1)
            data_types["min_value"] = min_value[0] if len(min_value) > 0 else None
            data_types["max_value"] = max_value[0] if len(max_value) > 0 else None
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
        else:
            col_rdd = col_rdd.filter(lambda x: get_type(x) == "DATE").map(lambda x: x.encode("utf-8")).cache()
            min_value = col_rdd.sortBy(lambda x: x).take(1)
            max_value = col_rdd.top(1)
            data_types["min_value"] = min_value[0] if len(min_value) > 0 else None
            data_types["max_value"] = max_value[0] if len(max_value) > 0 else None
        # save data
        column = dict()
        column["column_name"] = header[i]
        column["number_non_empty_cells"] = number_non_empty_cells
        column["number_empty_cells"] = number_empty_cells
        column["number_distinct_values"] = number_distinct_values
        column["frequent_values"] = frequent_values
        column["data_types"] = data_types
        output["columns"].append(column)
    # save to json file
    with open("./task1_data/%s.json" % dataset, 'w') as fp:
        json.dump(output, fp, cls=MyEncoder)
    print("%s processed OK" % dataset)


if __name__ == "__main__":
    # init
    sc = SparkContext()
    # get file and dir
    file = "/user/hm74/NYCOpenData/datasets.tsv"
    data_dir = file[:file.rfind("/") + 1]
    data_sets = sc.textFile(file).map(lambda x: x.split("\t")[0]).collect()
    # create result dir
    mkdir("./task1_data")
    # run profile for each dataset
    for dataset in data_sets:
        if not os.path.exists(data_dir + dataset + ".json"):
            profile(dataset)
        else:
            print("%s already processed" % dataset)
