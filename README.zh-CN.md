# m2w: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
基于Python将本地markdown推送和更新至Wordpress

:star2::star2::star2: 欢迎m2w 2.5正式投入使用!

中文教程: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)

## 内容列表

- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [项目展示](#项目展示)
- [Q&A](#Q&A)
- [维护者](#维护者)
- [使用许可](#使用许可)
- [相关仓库](#相关仓库)

## 背景

`m2w` 是一个简单易用的自动上传和更新 markdown 到 WordPress 的工具，支持REST API (`2.5+`) 和Password模式。

`m2w` 具有以下特点：

+ 支持REST API模式，比传统的Password模式更加安全。如果你喜欢，也可以继续使用Password模式。
+ 可以开心地保留原有的文件结构 (～￣▽￣)～ 。
+ 通过多个`legacy_*.json` 同时管理多个网站。
+ 只需要使用1个 python 脚本 `myblog.py` 而不是两个（`m2w 1.0` 中的 `update.py` 和 `upload.py`）。
+ 忽略重复的新markdown的上传操作（`v2.2.4+`）。

现阶段，REST API模式上传/更新文章的速度比Password模式慢，这可能是由于Wordfence等插件影响了REST API的工作效率。我们后续会修复该情况。

## 安装
1. poetry 安装方式

   >有关poetry的安装请查看官方文档[Introduction | Documentation | Poetry - Python dependency management and packaging made easy (python-poetry.org)](https://python-poetry.org/docs/)

   1. 下载随2.3.0更新上传的位于`poetry` 目录下的`pyproject.toml`和`poetry.lock`，放在一个你喜欢并且容易找到的文件夹
   2. 在目录下运行`poetry install`
   3. 查看接下来的使用教程部分

2. Anaconda安装

   > 建议使用 [Conda](https://conda.io/projects/conda/en/stable/user-guide/install/download.html) 来管理 Python 版本和相关依赖项。这是一个第3方示例教程：《[win10安装 Anaconda3](https://www.cnblogs.com/syushin/p/15113986.html)》。自己找找，教程很多的 (～￣▽￣)～ 

   依赖项：

   ```python
   # Python version
   python_requires='>=3.7.6'
   
   # Dependencies
   install_requires=[
       "python-frontmatter>=1.0.0",
       "markdown>=3.3.6",
       "python-wordpress-xmlrpc>=2.3",
       "httpx>=0.24.0"
   ]
   ```

3. 官方pip安装

   2022-12-10 之后，我将`m2w` 上传到 [PyPi](https://pypi.org/project/m2w/)，这样你只需要在Shell中运行`pip install m2w `即可安装。考虑到不同源同步延迟的可能性，你可以指定`m2w`的版本号和源：

   ```bash
   pip install -i https://pypi.org/simple m2w==2.5.2
   ```
   
4. 直接下载该仓库中的代码（不推荐）

   如果你采用这种方式，你还需要在环境中安装以下4个python包

   `python-frontmatter`,`markdown`,`python-wordpress-xmlrpc`, `httpx`

建议安装最新版本的`m2w 2`。

## 使用

### 允许REST API

> This step is needed only **when you want to use the REST API mode**.

+ 如果您使用wordfence之类的安全插件，请**启用WordPress应用程序密码**:

![WBrffVs5Ty](https://chevereto.hwb0307.com/images/2023/06/05/WBrffVs5Ty.png)

+ 创建一个新的REST API: 

![sq7kG7Vsqp](https://chevereto.hwb0307.com/images/2023/06/05/sq7kG7Vsqp.png)

+ 安全地保管该API。如果有必要，可以重新生成或删除:

![GddR0nP8mn](https://chevereto.hwb0307.com/images/2023/06/05/GddR0nP8mn.png)

### Use m2w

1. 安装m2w。
2. 在`path01`路径里修改 `myblog.py`。这里有一个[demo](https://github.com/huangwb8/m2w/blob/main/myblog.py)。创建 `<path02>/config/user.json` ，并且将`myblog.py`中的`path_m2w` 设置为 `<path02>` :

```python
path_m2w = '<path02>' # Absolute path of m2w
force_upload = False # Whether use force uploading
verbose = True # Whether report the process when using m2w
```

3. 定义 `<path02>/config/user.json`.  你可以添加多个网站，格式类似于 `web01`即可!  可以在[demo](https://github.com/huangwb8/m2w/blob/main/config/user.json)中了解更多细节。参数解释如下： 

  + **user.json** ——REST API模式： 


```json
"web01": {
        "domain": "https://domain-01.com",
        "username": "username-01",
        "application_password": "password-01",
        "path_markdown": [
            "E:/Github/m2w/@test/main",
            "E:/Github/m2w/@test/main2"
        ],
        "post_metadata": {
            "category": ["test"],
            "tag": ["test"],
            "status": "publish"
        },
        "path_legacy_json": "/config/legacy"
    }
```

+ **user.json** ——Password模式：


```json
"web01": {
        "domain": "https://domain-01.com",
        "username": "username-01",
        "password": "password-01",
        "path_markdown": [
            "E:/Github/m2w/@test/main",
            "E:/Github/m2w/@test/main2"
        ],
        "post_metadata": {
            "category": ["test"],
            "tag": ["test"],
            "status": "publish"
        },
        "path_legacy_json": "/config/legacy"
    }
```

  + **domain, username, application_password/password**:  WordPress帐户和密码（REST API）。 `application_password` 是REST API, `password`是帐户密码。如果两者共存，优先使用REST API。
  + **path_markdown**: 包含markdown文本的文件夹，可以有多个。
  + **post_metadata/path_legacy_json**: 不了解怎么设置的默认即可。

4. 准备工作完成后，直接运行这个命令即可：

```bash
python <path01>/myblog.py
```

## 项目展示

如下图所示，只需要一行`python myblog.py`，即可自动更新或上传markdown喔！

![Code_RVLd0mHbqc](https://chevereto.hwb0307.com/images/2023/06/05/Code_RVLd0mHbqc.gif)

## Q&A

1. Q：上传文章的时候报错`httpx.ConnectError: [Errno 11001] getaddrinfo failed`

   A：大概是网站地址没有写对，首先检查地址是否配置正确，请不要在`url`后面加资源地址如`https://xxx.com/xx/xx`,只填写到`xx.com`即可

2. Q：使用`REST_API`方式上传的时候可以正常获取**文章、tag**列表，但是上传却一直失败

   A：`REST_API`使用的是应用程序密码，而不是网站的登录密码，请检查**application_password**配置项是否类似`xxxx xxxx xxxx xxxx xxxx`的格式,在最新版本使用`Rest_API`失败后会自动尝试使用`Client`重新上传，所以不用担心。

3. Q：我的服务器在国内但是上传速度慢并且经常失败

   A：如果开了代理，请将自己的网站加入到过滤地址内，尤其是`CFW(clash for windows)`用户。

## 维护者

+ [@huangwb8](https://t.me/hwb0307)
+ [@FoxSuzuran](https://github.com/FoxSuzuran)

## 使用许可

m2w项目采用MIT license。详见[LICENSE](https://github.com/huangwb8/m2w/blob/main/license.txt)。

## 相关仓库

+ [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)
