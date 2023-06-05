# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8;Suzuran
# @File : m2w.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: VSCode
# @Reference: original

import time
import asyncio
import os.path
import shutil
import sys

from m2w import read_json_as_dict, md_detect, up, wp_xmlrpc
from m2w.rest_api import RestApi


# ===============================Parameters
# Please adjust the parameters according to the actual situation.
# Waring: config.ini and user.json should be in the same folder!
path_m2w = 'E:/Github/m2w/@test'
force_upload = False
verbose = True

# ===============================Program
async def main():

    path_user_json = path_m2w + '/config/user.json'
    websites = read_json_as_dict(path_user_json)

    for i in websites:
        # Select a WordPress website
        website = websites[i]

        # Parameters of the website
        domain = website['domain']
        username = website['username']
        path_markdown = website['path_markdown']
        post_metadata = website['post_metadata']
        path_legacy_json = path_m2w + website['path_legacy_json'] + '_' + i + '.json'

        # Whether use REST API mode
        use_rest_api = 'application_password' in website and len(website["application_password"]) > 10
        if not use_rest_api and 'password' not in website:
            print('API or password are missing. Please add one of them. Stop m2w!')
            sys.exit(0)
        elif not use_rest_api and 'password' in website : 
            rest_api = False
            application_password = None
        elif use_rest_api and 'password' in website:
            print("Warning: You have REST API. Password would be ignored. You can remove password in the 'user.json' to make the use of m2w safer!")
            rest_api = True
            application_password = website["application_password"]
        else:
            rest_api = True
            application_password = website["application_password"]

        # Connect the WordPress website
        print('========Website: ' + i)

        if os.path.exists(path_legacy_json):
            shutil.copyfile(path_legacy_json, path_legacy_json + "_temporary-copy")

        # Gather paths of brand-new and changed legacy markdown files
        res = md_detect(path_markdown, path_legacy_json,  verbose=verbose)
        md_upload = res['new']
        md_update = res['legacy']

        # Upload & Update
        if len(md_upload) > 0 or len(md_update) > 0:
            if rest_api:
                # REST API Mode
                if verbose: 
                    print("(ฅ´ω`ฅ) REST API Mode. Very safe!")
                rest = RestApi(
                    url=domain, wp_username=username, wp_password=application_password
                )
                try:
                    await rest.upload_article(
                        md_message=res,
                        post_metadata=post_metadata,
                        verbose=verbose,
                        force_upload=force_upload ,
                    )
                except Exception as e:
                    print(
                        "OOPS,The Rest-api failed. Please try again later!"
                    )
                    rest_api = False
                if os.path.exists(path_legacy_json + "_temporary-copy"):
                    os.remove(path_legacy_json + "_temporary-copy")
            else:
                # Legacy Password Mode
                if verbose: 
                    print("Σ( ° △ °|||)︴Legacy Password Mode. Not safe!")
                password = website["password"]
                # "password": "N*$Nh5Gyk9rnEt9GaQ7zq7A5f7hde$",
                client = wp_xmlrpc(domain, username, password)

                # Upload or Update
                try:
                    up(
                        client,
                        md_upload,
                        md_update,
                        post_metadata,
                        # Whether to force uploading a new post.
                        # `force_upload=False` is suggested for routine maintaining.
                        # `force_upload=True` is suggested for intensive uploading for a brand-new site.
                        force_upload=force_upload ,
                        # Whether to report running messages.
                        verbose=verbose,
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
            if verbose: 
                print('Without any new or changed legacy markdown files. Ignored.')


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"All done! Total time : {round(end - start, 3)}s")