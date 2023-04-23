# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8;Suzuran
# @File : m2w.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: VSCode
# @Reference: original
import logging
import time

import asyncio
import os.path
import shutil
import sys

from m2w import read_json_as_dict, md_detect, up, wp_xmlrpc
from m2w.config import ini_config, user_json_config
from m2w.rest_api import RestApi

# ===============================Program


async def main():
    con = ini_config()
    user_json_config(con)

    path_m2w = con["path"]["m2w_path"]
    path_user_json = path_m2w + '/config/user.json'
    websites = read_json_as_dict(path_user_json)

    for i in websites:
        # Select a WordPress website
        website = websites[i]

        # Parameters of the website
        domain = website['domain']
        username = website['username']

        application_password = None
        rest_api = False

        try:
            if len(website["application_password"]) > 10:
                application_password = website["application_password"]
                rest_api = True
        except Exception as e:
            logging.info(
                "application_password is not found or not right,try use client method"
            )
        password = website["password"]

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

        if os.path.exists(path_legacy_json):
            shutil.copyfile(path_legacy_json, path_legacy_json + "_temporary-copy")

        # Gather paths of brand-new and changed legacy markdown files
        res = md_detect(path_markdown, path_legacy_json, verbose=post_verbose)

        if rest_api:
            rest = RestApi(
                url=domain, wp_username=username, wp_password=application_password
            )
            try:
                await rest.upload_article(
                    md_message=res,
                    post_metadata=post_metadata,
                    verbose=post_verbose,
                    force_upload=post_force_upload,
                )
            except Exception as e:
                print(
                    "OOPS,The Rest-api failed,Application will attempt to use client method"
                )
                rest_api = False
        if not rest_api:
            client = wp_xmlrpc(domain, username, password)
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
                except Exception as e:
                    print("OOPS,The upload failed,Please Try again")
                    try:
                        os.remove(path_legacy_json)
                        os.rename(
                            path_legacy_json + "_temporary-copy", path_legacy_json
                        )
                    finally:
                        sys.exit(0)
            else:
                print('Without any new or changed legacy markdown files. Ignored.')
        if os.path.exists(path_legacy_json + "_temporary-copy"):
            os.remove(path_legacy_json + "_temporary-copy")


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"程序已结束,总用时: {end - start}")
