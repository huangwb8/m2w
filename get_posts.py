# -*- coding: utf-8 -*-
# @Time : 2021/11/19 16:00
# @Author : nefu-ljw
# @File : test-GetPosts.py
# @Software: PyCharm
# @Reference: https://python-wordpress-xmlrpc.readthedocs.io/en/latest/examples/posts.html#advanced-querying

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPosts
import m2w.json2

####===============================软件绝对路径===============================####

path_m2w = 'E:/Github/m2w' 

####================================正式工作=================================####

# User JSON
path_user_json = path_m2w + '/config/user.json' 
user = m2w.json2.read_json_as_dict(path_user_json)

# Client
xmlrpc = user['domain'] + '/xmlrpc.php'
client = Client(xmlrpc, user['username'], user['password'])

# get pages in batches of 20
offset = 0  # 每个batch的初始下标位置
batch = 20  # 每次得到batch个post，存入posts中
# 会得到所有文章，包括private(私密)、draft(草稿)状态的
all_cnt = 0
while True:
    posts = client.call(GetPosts({'number': batch, 'offset': offset}))
    all_cnt = all_cnt + len(posts)
    if len(posts) == 0:
        break  # no more posts returned
    for post in posts:
        #title = post.title
        print(post)
    offset = offset + batch
print('-----------------------------------------------END-----------------------------------------------')
print('There are %d articles in your WordPress.' % all_cnt)
