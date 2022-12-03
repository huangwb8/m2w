# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8
# @File : m2w.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: VSCode
# @Reference: original

####===============================m2w path

# Absolute path of m2w
path_m2w = 'E:/Github/m2w'

####===============================Dependency

from m2w.json2 import read_json_as_dict
from m2w.up import md_detect, up
from m2w.wp import wp_xmlrpc

####===============================Parameters

# Wheter use test mode (for developers only)
test_mode = False

# Main Configuration
if test_mode:
    # Test mode
    path_user_json = 'E:/Github/m2w/@test/config/user.json' 
    user = read_json_as_dict(path_user_json)
    path_legacy_json = 'E:/Github/m2w/@test/config/legacy' 
else:
    # Real mode
    path_user_json = path_m2w + '/config/user.json'
    user = read_json_as_dict(path_user_json)
    path_legacy_json = path_m2w + user['path_legacy_json'] 

# Other Configuration
path_markdown = user['path_markdown']
post_metadata = user['post_metadata']

####===============================Programe

if __name__ == '__main__':

    websites = user['websites']

    for i in websites:

        # Select a WordPress website
        website = websites[i]

        # Connect the WordPress website
        print('========')
        client = wp_xmlrpc(website['domain'], website['username'], website['password'])

        # # Gather paths of brand-new and changed legacy markdown files
        path_legacy_json2 = path_legacy_json + '_' + i + '.json'
        res = md_detect(path_markdown, path_legacy_json2, verbose = True)
        md_upload = res['new']
        md_update = res['legacy']

        # Upload or Update
        if len(md_upload) > 0 or len(md_update) > 0:
            print(i, ': With new or changed legacy markdown files.')
            up(client, md_upload, md_update, post_metadata, verbose = True)
        else:
            print(i, ': Without any new or changed legacy markdown files. Ignored.')