# -*- coding: utf-8 -*-
# @Time : 2021/11/20 9:42
# @Author : nefu-ljw; huangwb8
# @File : update.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: PyCharm
# @Reference: original

import re
import os
import sys
import frontmatter
import markdown
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost

try:
    from markdown_gfm_admonition import GfmAdmonitionExtension
    HAS_GFM_ADMONITION = True
except ImportError:
    HAS_GFM_ADMONITION = False

from m2w.math import MathExtension

# Fix the bug "module 'collections' has no attribute 'Iterable’"
if sys.version_info.minor >= 9:
    import collections.abc

    collections.Iterable = collections.abc.Iterable


def find_post(filepath, client):
    """
    find the post in WordPress by using filename in filepath as the searching title
    :param filepath: 更新用的文件路径
    :param client: 客户端
    :return True: if success
    """
    try:
        filename = os.path.basename(filepath)  # 例如：test(2021.11.19).md
        filename_prefix, filename_suffix = os.path.splitext(
            filename
        )  # 例如：test(2021.11.19) | .md

        # 目前只支持 .md 后缀的文件
        if filename_suffix != '.md':
            print('ERROR: not Markdown file')
            return None
        
        # get pages in batches of 20
        offset = 0  # 每个batch的初始下标位置
        batch = 20  # 每次得到batch个post，存入posts中
        while True:  # 会得到所有文章，包括private(私密)、draft(草稿)状态的
            posts = client.call(GetPosts({'number': batch, 'offset': offset}))
            if len(posts) == 0:
                return None  # no more posts returned
            for post in posts:
                title = post.title
                if title == filename_prefix:
                    return post
            offset = offset + batch
    except Exception as e:
        print('Reminder from Bensz(https://blognas.hwb0307.com) : ' + str(e))
        raise e
        # 正常退出
        # sys.exit(0)


def update_post_content(post, filepath, client):
    """
    update a post in WordPress with the content in file path
    :param post: 已发布的文章（WordPressPost类型），由find_post函数得到
    :param filepath: 更新用的文件路径
    :param client: 客户端
    :return True: if success
    """
    post_from_file = frontmatter.load(filepath)  # 读取文档里的信息
    extensions = ['markdown.extensions.fenced_code', 'tables', MathExtension()]
    if HAS_GFM_ADMONITION:
        extensions.append(GfmAdmonitionExtension())

    post_content_html = markdown.markdown(
        post_from_file.content, extensions=extensions
    ).encode(
        "utf-8"
    )  # 转换为html
    post.content = post_content_html  # 修改内容
    return client.call(EditPost(post.id, post))


def get_file_list(file_path):
    """
    python按时间排序目录下的文件
    """
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(
            dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x))
        )
        # print(dir_list)
        return dir_list
