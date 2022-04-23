# -*- coding: utf-8 -*-
# @Time : 2021/11/18 20:50
# @Author : nefu-ljw
# @File : test-Newpost.py
# @Software: PyCharm
# @Reference: original

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import m2w.json2

post = WordPressPost()  # 初始化post，我们要发表的文章就是post

# post的一些属性
post.title = "Test: This is the title"  # 标题
post.content = "Test: This is the content"  # 内容
post.post_status = 'publish'  # 类型（publish发布、draft草稿、private隐私）
post.terms_names = {
    'post_tag': ['test-tag1', 'test-tag2'],  # 标签(可以写多个)
    'category': ['test-category']  # 分类(可以写多个)
}  # 如果标签、分类没有的话会自动创建，有的话也不影响
post.comment_status = 'open'  # 开启评论

####===============================软件绝对路径===============================####

path_m2w = 'E:/Github/m2w' 

####================================正式工作=================================####

# User JSON
path_user_json = path_m2w + '/config/user.json' 
user = m2w.json2.read_json_as_dict(path_user_json)

# Client
xmlrpc = user['domain'] + '/xmlrpc.php'
client = Client(xmlrpc, user['username'], user['password'])
client.call(NewPost(post))
