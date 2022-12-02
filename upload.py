# -*- coding: utf-8 -*-
# @Time : 2021/11/19 0:50 
# @Author : nefu-ljw
# @File : upload-markdown-to-wordpress.py
# @Function: Upload new posts in WordPress with local Markdown files
# @Software: PyCharm
# @Reference: original


import os  # 用来遍历文件路径
import sys
import shutil
import frontmatter
import markdown
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import m2w.md5
import m2w.json2
import m2w.wp

####===============================软件绝对路径===============================####

path_m2w = 'E:/Github/m2w' 

####=================================设置作者的参数===============================####

# User JSON
path_user_json = path_m2w + '/config/user.json' 
user = m2w.json2.read_json_as_dict(path_user_json)

# Global
main = user['main'] # 总目录
symbol_new = user['symbol_new'] # 新文件所在目录
symbol_legacy = user['symbol_legacy'] # 历史文件所在目录

# User Configuration
path = main + '/' + symbol_new  # e.g. D:/PythonCode/post-wordpress-with-markdown/doc
domain = user['domain']  # e.g. https://jwblog.xyz（配置了SSL证书就用https，否则用http）
username = user['username']
password = user['password']

# Optional Configuration
post_metadata = user['post_metadata']

####=================================完成设置====================================####

def make_post(filepath, metadata):
    """
    make a WordPressPost for Client call
    :param filepath: 要发布的文件路径
    :param metadata: 字典类型
             包括 metadata['category']: 文章分类
                  metadata['tag']: 文章标签
                  metadata['status']: 有publish发布、draft草稿、private隐私状态可选
    :return WordPressPost: if success
            None: if failure
    """
    filename = os.path.basename(filepath)  # 例如：test(2021.11.19).md
    filename_suffix = filename.split('.')[-1]  # 例如：md
    filename_prefix = filename.replace('.' + filename_suffix, '')  # 例如：test(2021.11.19)；注意：这种替换方法要求文件名中只有一个".md"

    # 目前只支持 .md 后缀的文件
    if filename_suffix != 'md':
        return None

    # 1 通过frontmatter.load函数加载读取文档里的信息，包括元数据
    post_from_file = frontmatter.load(filepath)

    # 2 markdown库导入内容
    post_content_html = markdown.markdown(post_from_file.content, extensions=['markdown.extensions.fenced_code'])
    post_content_html = post_content_html.encode("utf-8")

    # 3 将本地post的元数据暂存到metadata中
    metadata['title'] = filename_prefix  # 将文件名去掉.md后缀，作为标题
    # metadata['slug'] = metadata['title']  # 别名
    metadata_keys = metadata.keys()
    # 如果post_from_file.metadata中的属性key存在，那么就将metadata[key]替换为它
    for key in metadata_keys:
        if key in post_from_file.metadata:  # 若md文件中没有元数据'category'，则无法调用post.metadata['category']
            metadata[key] = post_from_file.metadata[key]

    # 4 将metadata中的属性赋值给post的对应属性
    post = WordPressPost()  # 要返回的post
    post.content = post_content_html
    post.title = metadata['title']
    # post.slug = metadata['slug']
    post.post_status = metadata['status']
    post.terms_names = {
        'category': metadata['category'],
        'post_tag': metadata['tag']
    }
    post.comment_status = 'open'  # 开启评论
    return post


def push_post(post, client):
    """
    上传post到WordPress网站
    :param post: 要发布的文章（WordPressPost类型），由make_post函数得到
    :param client: 客户端
    :return True: if success
    """
    return client.call(NewPost(post))


def get_filepaths(path):
    """
    如果path是目录路径，递归遍历path目录下的所有文件，将所有文件路径存入filepaths
    如果path是文件路径，直接将单个文件路径存入filepaths
    :param path: 你要上传的目录路径或文件路径（绝对路径）
    :return filepaths: 该目录下的所有子文件或单个文件的绝对路径
            None: wrong path
    """
    filepaths = []
    if os.path.isdir(path):  # 当前路径是目录
        for now_dirpath, child_dirnames, child_filenames in os.walk(path):
            for filename in child_filenames:
                filepath = os.path.join(now_dirpath, filename)
                filepaths.append(filepath)
        return filepaths
    elif os.path.isfile(path):  # 当前路径是文件
        return [path]
    else:  # wrong path
        return None


if __name__ == '__main__':
    
    # Start Work
    # print('----------------------------------------------START----------------------------------------------')
    filepaths = get_filepaths(path)
    if filepaths is None:
        print('FAILURE: wrong path')
        sys.exit(1)

    # client = Client(domain + '/xmlrpc.php', username, password)  # 客户端
    client = m2w.wp.wp_xmlrpc(domain, username, password)
    
    md_cnt = 0
    all_cnt = len(filepaths)
    process_number = 0
    failpaths = []  # 存储上传失败的文件路径
    for filepath in filepaths:
        process_number = process_number + 1
        post = make_post(filepath, post_metadata)
        filename = os.path.basename(filepath)
        if post is not None:
            push_post(post, client)
            md_cnt = md_cnt + 1
            shutil.move(filepath, filepath.replace(symbol_new, symbol_legacy)) # 上传完成后，将文件转移到legacy目录
            print('Process number: %d/%d  SUCCESS: Push "%s" completed!' % (process_number, all_cnt, filename))
        else:
            failpaths.append(filepath)
            print('Process number: %d/%d  WARNING: Can\'t push "%s" because it\'s not Markdown file.' % (process_number, all_cnt, filename))
    # print('-----------------------------------------------END-----------------------------------------------')
    print('SUCCESS: %d files have been pushed to your WordPress.' % md_cnt)

    if len(failpaths) > 0:
        print('WARNING: %d files haven\'t been pushed to your WordPress.' % len(failpaths))
        print('\nFailure to push these file paths:')
        for failpath in failpaths:
            print(failpath)