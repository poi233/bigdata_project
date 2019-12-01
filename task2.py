# -*- coding: UTF-8 -*-
import json
import os
import re

from pyspark.sql import SparkSession


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def check_semantic_type(col, input_df):
    col = str(col).replace("_", " ").lower()
    # Person Name
    if ('first' in col or 'last' in col) and 'name' in col:
        pass
    # Business Name
    if 'business' in col and 'name' in col:
        pass
    # Phone Number
    if 'phone' in col:
        pass
    # Address
    # Street Name
    # City
    # Neighborhood
    # LAT/LON coordinates
    # Zip code
    if 'zip' in col:
        pass
    # Borough
    if 'boro' in col:
        pass
    # School name
    if col == 'school' or ('school' in col and 'name' in col):
        pass
    # Color
    if 'color' in col:
        pass
    # Car Make
    if 'make' in col:
        pass
    # City Agency
    # Area of study
    # subjects in school
    # school level
    if 'school' in col and 'level' in col:
        pass
    # college/university names
    # websites
    if 'website' in col:
        pass
    # building classification
    # vehicle type
    if 'vehicle' in col and 'type' in col:
        pass
    # type of location
    # parks/playground
    if 'park' in col and 'name' in col:
        pass


def init_files():
    count = 0
    data = dict()
    with open('cluster2.txt') as file:
        origins = [file_name.strip()[1:-1] for file_name in file.readline().split(",")]
        for origin in origins:
            if origin.split(".")[0] not in data:
                data[origin.split(".")[0]] = []
            data[origin.split(".")[0]].append(origin.split(".")[1])
            count += 1
    print("total columns = %s" % count)
    return data


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("bigdata_project") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    # get file and dir
    # /user/hm74/NYCOpenData/c284-tqph.tsv.gz
    mkdir("./task2_data")
    data_dir = "/user/hm74/NYCOpenData/"
    files = init_files()
    print('total %s files' % len(files))
    count = 1
    for file in files:
        print("%s start" % file)
        full_file = data_dir + file + ".tsv.gz"
        opendata_df = spark.read.format('csv').options(header='true', inferschema='true', sep='\t').load(full_file)
        for column in files[file]:
            pattern = re.compile('^' + column.replace("_", "(.*)") + '$')
            for col in opendata_df.columns:
                if re.match(pattern, col):
                    to_save = dict()
                    to_save[file] = dict()
                    column_df = opendata_df.select(col).sample(False, 0.3)
                    column_to_save = column_df.rdd.map(lambda x: x[0]).take(20)
                    to_save[file][col] = column_to_save
                    with open("./task2_data/" + file + "." + column + ".json", 'w') as fp:
                        json.dump(to_save, fp, cls=MyEncoder)
                    print("%s %s %s ok" % (file, column, count))
                    count += 1
        print("%s finish" % file)
