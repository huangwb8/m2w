# m2w: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
基于Python将本地markdown推送和更新至Wordpress，支持REST API和Password模式

:star2::star2::star2: 欢迎m2w 2.5正式投入使用!

中文教程: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)

## 内容列表

- [m2w: Markdown to WordPress](#m2w-markdown-to-wordpress)
  - [内容列表](#内容列表)
  - [背景](#背景)
  - [安装](#安装)
  - [使用](#使用)
    - [开启 REST API](#开启-rest-api)
  - [项目展示](#项目展示)
  - [Q\&A](#qa)
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

## 安装

> 推荐使用[Miniconda](https://docs.conda.io/en/latest/miniconda.html)来管理Python版本和相关依赖。

这是所需的依赖项：

```python
# Python 版本要求
python_requires='>=3.7.6'

# 依赖项
install_requires=[
    "python-frontmatter>=1.0.0",
    "markdown>=3.3.6",
    "python-wordpress-xmlrpc>=2.3",
    "httpx>=0.24.0"
]
```

在2022年12月10日之后，`m2w`已经上传到了[PyPi](https://pypi.org/project/m2w/)。要安装 `m2w`，只需要在您的 shell/conda 环境中运行以下代码：

```
pip install m2w
```

您也可以直接从这个仓库下载 `m2w`。使用方法完全相同。

在安装 `m2w` 时，您可以指定版本或资源：

```bash
pip install -i https://pypi.org/simple m2w==2.5.12
```

通常建议使用最新版本的 `m2w`。


## 使用

在 `path01` 目录下创建文件夹 `config`，并在文件夹创建 `user.json`，示例如下

```json
"web01": {
        "domain": "https://domain-01.com",
        "username": "username-01",
        "application_password": "password-01",
        // "password": "password-01",
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

参数说明：
  - `domain`: WordPress 站点的域名
  - `username`: WordPress 账户
  - `application_password`: 应用程序密码（推荐），与 `password` 二选一即可。获取方式见下文[开启 REST API](#开启-rest-api)
  - `password`: 账户密码，与 `application_password` 二选一即可，如果二者共存，优先使用 REST API。
  - `path_markdown`: 包含 markdown 文本的文件夹，可以有多个。
  - `post_metadata/path_legacy_json`: 不了解怎么设置的默认即可。

创建脚本 `myblog.py`，这里有一个[示例](https://github.com/huangwb8/m2w/blob/main/myblog.py)，需要将 `path_m2w` 修改为 `config` 文件夹所在的路径。

```python
path_m2w = '<path02>' # config文件夹的路径
```

准备工作完成后，直接运行这个命令即可：

```bash
python <path01>/myblog.py
```

### 开启 REST API

> 如果你想使用 REST API 模式，则需要这一步。

+ 如果您使用 wordfence 之类的安全插件，请**启用 WordPress 应用程序密码**:

   ![WBrffVs5Ty](https://chevereto.hwb0307.com/images/2023/06/05/WBrffVs5Ty.png)

+ 创建一个新的 REST API: 

   ![sq7kG7Vsqp](https://chevereto.hwb0307.com/images/2023/06/05/sq7kG7Vsqp.png)

+ 安全地保管该API。如果有必要，可以重新生成或删除:

   ![GddR0nP8mn](https://chevereto.hwb0307.com/images/2023/06/05/GddR0nP8mn.png)


## 项目展示

如下图所示，只需要一行`python myblog.py`，即可自动更新或上传markdown喔！

![image-20230609173358533](https://chevereto.hwb0307.com/images/2023/06/09/image-20230609173358533.png)

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
