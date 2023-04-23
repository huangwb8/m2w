#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/2/16 23:02
# @Author  : Suzuran
# @FileName: config.py
# @Software: PyCharm

import os
import sys
import configparser
import json


class MyCfgIni(configparser.ConfigParser):
    def to_dict(self):
        return dict(self._sections)


def ini_config() -> dict:
    """
    初始化ini配置文件
    @return: 配置文件内容的字典
    """
    con = MyCfgIni()
    if not os.path.exists("config.ini"):
        con["path"] = {"m2w_path": os.path.abspath("")}
        con["upload"] = {"force_upload": "False", "verbose": "True"}

        with open("config.ini", "w", encoding="utf-8") as cfg:
            con.write(cfg)
        print("配置文件config.ini已在目录下生成,请填写配置后重新启动程序")
        sys.exit(0)
    else:
        con.read("config.ini", encoding="utf-8")
        return con.to_dict()


def user_json_config(con: dict) -> None:
    """
    初始化user.json配置文件
    @param con: ini文件字典
    """
    if not os.path.exists(con["path"]["m2w_path"] + "/config/user.json"):
        if not os.path.exists(con["path"]["m2w_path"] + "/config"):
            os.mkdir(con["path"]["m2w_path"] + "/config")
        with open(
            con["path"]["m2w_path"] + "/config/user.json", "w", encoding="utf-8"
        ) as user_cfg:
            json.dump(
                {
                    "web_test": {
                        "domain": "https://domain-01.com",
                        "username": "username-01",
                        "password": "password-01",
                        "application_password": "",
                        "path_markdown": [
                            "E:/Github/m2w/@test/main",
                            "E:/Github/m2w/@test/main2",
                        ],
                        "post_metadata": {
                            "category": ["test"],
                            "tag": ["test"],
                            "status": "publish",
                        },
                        "path_legacy_json": "/config/legacy",
                    },
                },
                user_cfg,
                indent=4,
            )
            print(f"配置文件user.json已在目录{con['path']['m2w_path']}\\config下生成,请填写配置后重新启动程序")
            sys.exit(0)
