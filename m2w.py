# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8
# @File : m2w.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: VSCode
# @Reference: original

####===============================m2w path

# Absolute path of m2w
path_m2w = 'E:/Github/m2w/@test' # /@test

####===============================Dependency

from m2w.json2 import read_json_as_dict
from m2w.up import md_detect, up
from m2w.wp import wp_xmlrpc

####===============================Programe

if __name__ == '__main__':

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

        # Connect the WordPress website
        print('========Website: ' + i)
        client = wp_xmlrpc(domain, username, password)

        # Gather paths of brand-new and changed legacy markdown files
        res = md_detect(path_markdown, path_legacy_json, verbose = True)
        md_upload = res['new']
        md_update = res['legacy']

        # Upload or Update
        if len(md_upload) > 0 or len(md_update) > 0:
            up(
                client, md_upload, md_update, post_metadata,
                # Whether to force uploading a new post. `force_upload=False` is suggested.
                force_upload = False, 
                # Whether to report running messages.
                verbose = True
            )
        else:
            print('Without any new or changed legacy markdown files. Ignored.')