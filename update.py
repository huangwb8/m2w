# -*- coding: utf-8 -*-
# @Time : 2021/11/20 9:42
# @Author : nefu-ljw; huangwb8
# @File : update.py
# @Function: Update an existing post in WordPress with a local Markdown file
# @Software: PyCharm
# @Reference: original

import glob
import os
import sys
import frontmatter
import markdown
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPosts, EditPost
import m2w.md5
import m2w.json2


####===============================软件绝对路径===============================####

path_m2w = 'E:/我的坚果云/样式备份/网站/m2w_2'

####=================================设置作者的参数===========================####

# User JSON
path_user_json = path_m2w + '/config/user.json' 
user = m2w.json2.read_json_as_dict(path_user_json)
# print('path_user_json: ', path_user_json)

# Global
main = user['main'] # 总目录
# print('main: ', main)

symbol_legacy = user['symbol_legacy'] # 历史文件所在目录


# User Configuration
domain = user['domain']  # e.g. https://jwblog.xyz（配置了SSL证书就用https，否则用http）
username = user['username']
password = user['password']
path_legacy_json = path_m2w + user['path_legacy_json']
# print('path_legacy_json: ', path_legacy_json)

# 待更新markdown所在目录
path_legacy = main + '/' + symbol_legacy + '/' # e.g. D:/PythonCode/post-wordpress-with-markdown/doc/test.md
# print('path_legacy: ', path_legacy)

####=================================完成设置====================================####

def find_post(filepath, client):
    """
    find the post in WordPress by using filename in filepath as the searching title
    :param filepath: 更新用的文件路径
    :param client: 客户端
    :return True: if success
    """
    try:
        filename = os.path.basename(filepath)  # 例如：test(2021.11.19).md
        filename_suffix = filename.split('.')[-1]  # 例如：md
        filename_prefix = filename.replace('.' + filename_suffix, '')  # 例如：test(2021.11.19)；注意：这种替换方法要求文件名中只有一个".md"
        # 目前只支持 .md 后缀的文件
        if filename_suffix != 'md':
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
        # 正常退出
        sys.exit(0)

def update_post_content(post, filepath, client):
    """
    update a post in WordPress with the content in file path
    :param post: 已发布的文章（WordPressPost类型），由find_post函数得到
    :param filepath: 更新用的文件路径
    :param client: 客户端
    :return True: if success
    """
    post_from_file = frontmatter.load(filepath)  # 读取文档里的信息
    post_content_html = markdown.markdown(post_from_file.content,
                                          extensions=['markdown.extensions.fenced_code']).encode("utf-8")  # 转换为html
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
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        # print(dir_list)
        return dir_list

def wp_xmlrpc(domain,username, password):
    """
    错误控制相关的Client函数
    """
    try:
        client = Client(domain + '/xmlrpc.php', username, password)  # 客户端
        print('SUCCESS to connect' + domain)
        return client
    except Exception as e:
        print('Reminder from Bensz(https://blognas.hwb0307.com) : ' + str(e))
        # 正常退出
        sys.exit(0)

if __name__ == '__main__':

    # Start Work
    # if not os.path.isfile(filepath):
    #     print('FAILURE: not file path')
    #     sys.exit(1)

    # 访问WordPress xmlrpc.php
    client = wp_xmlrpc(domain,username, password)

    # 新旧文件对比
    if os.path.isfile(path_legacy_json):
        # 并非初次上传
        legacy_md5_old = m2w.json2.read_json_as_dict(path_legacy_json)
        markdown_md5 = m2w.md5.md5_legacy_markdown(path_legacy, path_legacy_json)
        markdown_md5_filter = markdown_md5

        # 交集
        # print(sorted(markdown_md5.keys()))
        # print(sorted(legacy_md5_old.keys()))
        intersect_key = set(sorted(markdown_md5.keys())) & set(sorted(legacy_md5_old.keys()))
        #print(intersect_key)

        # 验证md5
        for i in intersect_key:
            if legacy_md5_old[i] == markdown_md5[i]:
                markdown_md5_filter.pop(i)
            else:
                print('Content changed!: ', i)
    else:
        print('Initial update...')
        markdown_md5_filter = m2w.md5.md5_legacy_markdown(path_legacy, path_legacy_json)

    # print(path_legacy)
    # print(path_legacy_json)
    # print(sorted(markdown_md5.keys()))
    # print(sorted(markdown_md5_filter.keys()))

    # 上传有变化的文件
    if len(sorted(markdown_md5_filter.keys())) == 0:
        print('Legacy: None of markdowns had any changes.')
    else:
        for filepath in sorted(markdown_md5_filter.keys()):
            # client = Client(domain + '/xmlrpc.php', username, password)  # 客户端
            post = find_post(filepath, client)
            if post is not None:
                ret = update_post_content(post, filepath, client)
                if ret:
                    print('SUCCESS to update the file: "%s"' % filepath)
                else:
                    print('FAILURE to update the file: "%s"' % filepath)
            else:
                print('FAILURE to find the post. Please check your User Configuration and the title in your WordPress.')
