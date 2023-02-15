# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8;Suzuran
# @File : m2w.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: VSCode
# @Reference: original

import configparser
import json
import os.path
import shutil
import sys

from m2w import read_json_as_dict, md_detect, up, wp_xmlrpc

# ===============================Program

if __name__ == '__main__':
    con = configparser.ConfigParser()
    if not os.path.exists("config.ini"):
        con["path"] = {"m2w_path": os.path.abspath("")}
        con["upload"] = {"force_upload": "False", "verbose": "True"}

        with open("config.ini", "w", encoding="utf-8") as cfg:
            con.write(cfg)
        print("配置文件config.ini已在目录下生成,请填写配置后重新启动程序")
        sys.exit(0)
    con.read("config.ini")
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

    path_m2w = con["path"]["m2w_path"]

    path_user_json = path_m2w + '/config/user.json'
    websites = read_json_as_dict(path_user_json)

    for i in websites:
        # Select a WordPress website
        website = websites[i]

        # Parameters of the website
        domain = website['domain']
        username = website['username']
        password = website['password']
        path_markdown = website['path_markdown']
        post_metadata = website['post_metadata']
        path_legacy_json = path_m2w + website['path_legacy_json'] + '_' + i + '.json'

        post_verbose = (
            con["upload"]["verbose"] == str(True)
            if con["upload"]["verbose"].lower() in ["true", "false"]
            else True
        )
        post_force_upload = (
            con["upload"]["force_upload"] == str(True)
            if con["upload"]["force_upload"].lower() in ["true", "false"]
            else False
        )

        # Connect the WordPress website
        print('========Website: ' + i)
        client = wp_xmlrpc(domain, username, password)

        # Gather paths of brand-new and changed legacy markdown files
        if os.path.exists(path_legacy_json):
            shutil.copyfile(path_legacy_json, path_legacy_json + "_temporary-copy")

        res = md_detect(path_markdown, path_legacy_json, verbose=post_verbose)
        md_upload = res['new']
        md_update = res['legacy']

        # Upload or Update
        if len(md_upload) > 0 or len(md_update) > 0:
            try:
                up(
                    client,
                    md_upload,
                    md_update,
                    post_metadata,
                    # Whether to force uploading a new post.
                    # `force_upload=False` is suggested for routine maintaining.
                    # `force_upload=True` is suggested for intensive uploading for a brand-new site.
                    force_upload=post_force_upload,
                    # Whether to report running messages.
                    verbose=post_verbose,
                )
            except:
                try:
                    os.remove(path_legacy_json)
                    os.rename(path_legacy_json + "_temporary-copy", path_legacy_json)
                finally:
                    sys.exit(0)
        else:
            print('Without any new or changed legacy markdown files. Ignored.')
        if os.path.exists(path_legacy_json + "_temporary-copy"):
            os.remove(path_legacy_json + "_temporary-copy")
