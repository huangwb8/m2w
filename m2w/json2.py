#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def read_json_as_dict(path_file):
    """
    读取json文件并生成dict
    """
    # rb可防止中文乱码
    with open(path_file, "rb") as json_file:
        json_dict = json.load(json_file)
        return json_dict


def save_dict_as_json(json_dict, path_file):
    """
    将dict保存为json文件
    """
    with open(path_file, "w") as json_file:
        json.dump(json_dict, json_file, indent=4)
