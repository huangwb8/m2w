# -*- coding: utf-8 -*-
# @Time : 2022/12/03 16:42
# @Author : huangwb8
# @File : wp.py
# @Function: m2w project
# @Software: VSCode
# @Reference: original

import sys
from wordpress_xmlrpc import Client


def wp_xmlrpc(domain, username, password):
    """
    ### Description
    The Client function with error control

    ### Parameters
    + domain: The domain of the WordPress site.
    + username: The user name of the WordPress site.
    + password: The password of the user name.

    ### Return
    A Client object
    """
    try:
        client = Client(domain + '/xmlrpc.php', username, password)  # 客户端
        print('SUCCESS to connect to your WordPress website: ' + domain)
        return client
    except Exception as e:
        print('FAILED to connect to your WordPress website: ' + str(e))
        # 正常退出
        sys.exit(0)
