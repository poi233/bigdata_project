# -*- coding: UTF-8 -*-
import json
import os
import re

def init_files():
    with open('cluster2.txt') as file:
        origins = [file_name.strip()[1:-1] for file_name in file.readline().split(",")]
    return origins


if __name__ == "__main__":
    # get file and dir
    data_dir = "./NYCColumns/"
    all_files = os.listdir(data_dir)
    valid_files = list(set(init_files()))
    print(len(valid_files))
    print(len(all_files))
    for all_file in all_files:
        if all_file not in valid_files:
            os.remove(data_dir + all_file)
