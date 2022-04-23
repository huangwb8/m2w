# m2w: Markdown to Wordpress

## 简介

Push `Markdown` to `Wordpress` dashboard via Python

基于Python将本地markdown推送至Wordpress后台

## 前言

主要是在[nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)的基础上进行了一些改进。

有以下特点：

+ 通过`config/user.json`文件来定义用户属性。
+ 将新旧的markdown分开为`new`和`legacy`两个目录保存。
+ 在`new`目录中的所有文件都会上传。
+ 在`legacy`目录中，批量上传有更新的旧markdown文件，自动忽略没有更新的旧markdown文件。机制是通过检测`md5`值判断文件有没有变化。上一次更新后，legacy文件的md5值将会保存在`config/legacy.json`中。

## 准备工作

+ 运行环境：Python 3.7或以上

+ 安装依赖：

```
pip3 install python-frontmatter
pip3 install markdown
pip3 install python-wordpress-xmlrpc
```

+ 自定义`config/user.json`文件：

```json
{
    // 博客文件主目录的绝对路径
    "main": "E:/Github/m2w/blog",
    
    // 博客文件主目录的绝对路径的new文件夹，一般不用改。
    "symbol_new": "new",
    
    // 博客文件主目录的绝对路径的legacy文件夹，一般不用改。
    "symbol_legacy": "legacy",
    
    // 博客域名、用户名、密码
    "domain": "https://blog.domain.com",
    "username": "user",
    "password": "user_password",
    
    // 自定义。默认上传的分类、标签和状态
    "post_metadata": {
        "category": ["test"],
        "tag": ["test"],
        "status": "publish"
    },
    
    // 不用改
    "path_legacy_json": "/config/legacy.json"
}
```

+ 将所有脚本的`path_m2w`参数改成你存放本仓库目录的绝对路径。比如我这个目录是放在`'E:/Github/m2w'`，可以设置：

  ```python
  path_m2w = 'E:/Github/m2w'
  ```

+ `get_posts.py`、`new_posts.py`只用于测试`user.json`是否用效。平时并不需要。

## 使用

+ 博客的目录结构类似于：

```
blog
├──legacy
└──new
```

+ 在`new`文件夹写新的markdown

+ 运行`upload.py`用于上传新markdown

+ 如果`legacy`文件夹的内容有更改，运行`update.py`更新。

所有脚本（包括测试脚本）用法都是类似的：

```bash
python3 <脚本>.py
```

一般我都是在vscode中打开脚本整个运行。PyCharm之类的应该也是类似吧！

效果特性也和原作一样，并未改动。

## 说明

我是站在巨人的肩膀上，自己是个菜鸡(￣△￣；)。

感觉可以做得更细致，不过自己能力有限。以后慢慢改进吧！

其它更详细地说明请看：[nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)
