#!/usr/bin/env python
# -*- coding: utf-8 -*-
# From: https://www.jb51.net/article/202775.htm

import hashlib
import os
import glob
from m2w.json2 import save_dict_as_json


def get_file_md5(file_name):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(file_name, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  # 更新md5对象

    return m.hexdigest()  # 返回md5对象


def get_str_md5(content):
    """
    计算字符串md5
    :param content:
    :return:
    """
    m = hashlib.md5(content)  # 创建md5对象
    return m.hexdigest()


def md5_legacy_markdown(path_legacy, path_legacy_json):
    """
    总结legacy的md文件
    """
    dict = {}
    md_files = glob.glob(os.path.join(path_legacy, "*.md"))

    for i in md_files:
        dict[i] = get_file_md5(i)
    save_dict_as_json(dict, path_legacy_json)

    return dict
