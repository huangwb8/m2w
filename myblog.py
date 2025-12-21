# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8; Suzuran
# @File : myblog.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: VSCode
# @Reference: original

# ===============================Dependency
from m2w import read_json_as_dict, up
import sys
import asyncio
import time


# ===============================Parameters
# Please adjust the parameters according to the actual situation.

# m2w version: 2.5.7+

# The path of the config folder, where contains user.json and legacy*.json
path_m2w = "E:/我的坚果云/样式备份/网站/m2w 2.5"

# Whether to force uploading a new post.
# `force_upload=False` is suggested for routine maintaining.
# `force_upload=True` is suggested for intensive uploading for a brand-new site.
force_upload = False

# Whether to report running messages.
verbose = True

# Whether to update the last update time of the post. Only work in REST API mode.
last_update_time_change = False

# Retry time when meeting failure
max_retries = 10

# REST API HTTP timeout (seconds). Default 30s; increase for slow hosts.
rest_timeout = 30


# ===============================Program
async def main():
    path_user_json = path_m2w + "/config/user.json"
    websites = read_json_as_dict(path_user_json)

    for i in websites:
        # Select a WordPress website
        website = websites[i]

        # Parameters of the website
        domain = website["domain"]
        username = website["username"]
        path_markdown = website["path_markdown"]
        post_metadata = website["post_metadata"]
        path_legacy_json = path_m2w + website["path_legacy_json"] + "_" + i + ".json"

        # Whether use REST API mode
        use_rest_api = (
            "application_password" in website
            and len(website["application_password"]) > 10
        )
        if not use_rest_api and "password" not in website:
            print("API or password are missing. Please add one of them. Stop m2w!")
            sys.exit(0)
        elif not use_rest_api and "password" in website:
            rest_api = False
            application_password = None
            password = website["password"]
        elif use_rest_api and "password" in website:
            print(
                "Warning: You have REST API. Password would be ignored. You can remove password in the 'user.json' to make the use of m2w safer!"
            )
            rest_api = True
            application_password = website["application_password"]
            password = None
        else:
            rest_api = True
            application_password = website["application_password"]
            password = None

        # Connect the WordPress website
        print("========Website: " + i)
        await up(
            # The path of files
            path_markdown = path_markdown, 
            path_legacy_json = path_legacy_json,

            # Website data
            domain = domain, 
            username = username, 
            password = password, 
            application_password = application_password, 
            post_metadata = post_metadata,

            # Parameters
            last_update_time_change = last_update_time_change, 
            force_upload = force_upload, 
            verbose = verbose, 
            rest_api = rest_api, 
            max_retries = max_retries,
            rest_timeout = rest_timeout
        )


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"All done! Total time : {round(end - start, 3)}s")
