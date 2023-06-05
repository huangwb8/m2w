# m2w: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
基于Python将本地markdown推送和更新至Wordpress

Demo: [https://blognas.hwb0307.com](https://blognas.hwb0307.com)

Tutorial: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践](https://blognas.hwb0307.com/linux/docker/689)。

![](https://chevereto.hwb0307.com/images/2022/05/27/Code_6OcltCZ2le.gif)

## 内容列表

- [背景](#背景)
- [安装](#安装)
- [使用说明](#使用说明)
- [相关仓库](#相关仓库)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)

## 背景

> 感谢[cye](https://github.com/cye18)推荐[WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools)项目作为WordPress博客管理的替代平台之一，其基于Github Actions，类似于Hexo。感兴趣的小伙伴可以了解一波！

最近玩起了WordPress博客，所以想找一个一键更新markdown的工具来用。找了好久，感觉[nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)这个项目可以用。不过这个项目在更新旧的Markdown文档的自动化程度不高；而且在不同的脚本之间要重复地填写用户信息。

本项目主要是在[nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)的基础上进行了小小的改进，有以下特点：

+ 通过`config/user.json`文件来托管用户属性。
+ 将新旧的markdown分开为`new`和`legacy`两个目录保存。
+ 在`new`目录中的所有文件都会上传。
+ 在`legacy`目录中，批量上传有更新的旧markdown文件，自动忽略没有更新的旧markdown文件。机制是通过检测`md5`值判断文件有没有变化。上一次更新后，legacy文件的md5值将会保存在`config/legacy.json`中。

## 安装

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

## 使用说明

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

这里展示一下`upload.py`的界面：

![image-20220424134824223](https://chevereto.hwb0307.com/images/2022/04/24/image-20220424134824223.png)

这里展示一下`update.py`的界面：

![image-20220424125654213](https://chevereto.hwb0307.com/images/2022/04/24/image-20220424125654213.png)

## 相关仓库

+ [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)

## 维护者

[@huangwb8](https://t.me/hwb0307)

## 如何贡献

非常欢迎你的加入！[提一个 Issue](https://github.com/huangwb8/m2w/issues/new) 或者提交一个 Pull Request。


m2w遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范。

### 贡献者

暂无。欢迎加入！


## 使用许可

因为参考仓库的作者并未给出license，所以我暂时也不加。我会询问[@nefu-ljw](https://github.com/nefu-ljw)的建议。
