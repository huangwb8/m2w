# m2w 2: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
基于Python将本地markdown推送和更新至Wordpress

教程: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)。

## 内容列表

- [展示](#展示)
- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [相关仓库](#相关仓库)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)

## 背景

`m2w` 是一个简单易用的自动上传和更新 markdown 到 WordPress 的工具，`m2w 1.0` 的开发工作已经在 `v1.0.7` 中被冻结。 `m2w 1.0` 对大多数人来说已经足够强大了，但有些特性对使用者不太友好：

+ 必须分配旧的或新的路径来存储博文，这意味着使用者无法随意放置文件。
+ 无法同时对多个站点进行管理。

你仍然可以找到m2w 1.0的使用说明（[中](https://github.com/huangwb8/m2w/blob/main/v1/README.zh-CN.md)/[英](https://github.com/huangwb8/m2w/blob/main/v1/README.md)），但我原则上不再维护`m2w 1.0`了。

现在，更强大的`m2w 2`来和大家见面啦！`m2w 2` 具有以下特点：

+ 与 `m2w 1.0` 相比，使用 和`config/user.json` 略微不同的方式维护用户信息。
+ 可以开心地保留原有的文件结构 (～￣▽￣)～ 。
+ 通过多个`legacy_*.json` 同时管理多个网站。
+ 只需要使用1个 python 脚本 `m2w.py` 而不是两个（`m2w 1.0` 中的 `update.py` 和 `upload.py`）。
+ 忽略重复的新markdown的上传操作（`v2.2.4+`）。该特性对于用户从`m2w 1.0`升级到`m2w 2`十分友好！
+ 像m2w 1.0 稳定且好用！

## 安装

> 建议使用 [Conda](https://conda.io/projects/conda/en/stable/user-guide/install/download.html) 来管理 Python 版本和相关依赖项。这是一个第3方示例教程：《[win10安装 Anaconda3](https://www.cnblogs.com/syushin/p/15113986.html)》。自己找找，教程很多的 (～￣▽￣)～ 

依赖项：

```python
# Python 3.7.4 is the version I use m2w. I'm not sure whether it could work well in more advanced Python versions.
python_requires='>=3.7.4'

# Dependencies
install_requires=[
    "python-frontmatter>=1.0.0",
    "markdown>=3.3.6",
    "python-wordpress-xmlrpc>=2.3"
]
```

2022-12-10 之后，我将`m2w 2` 上传到 [PyPi](https://pypi.org/project/m2w/)，这样你只需要在Shell中运行`pip install m2w `即可安装。

考虑到不同源同步延迟的可能性，你可以指定`m2w 2`的版本号和源：

```bash
pip install -i https://pypi.org/simple m2w==2.2.10
```

建议安装最新版本的`m2w 2`。

## 使用

1. 通过`pip`或这个Github repotory安装 m2w。
2. 新建文件`<path01>/m2w.py`文件，这是一个[示例](https://github.com/huangwb8/m2w/blob/main/m2w.py)。将`m2w.py`文件中的`path_m2w`赋值为`<path02>`

```python
# Absolute path of m2w
path_m2w = '<path02>'
```

3. 新建文件`<path02>/config/user.json`，这是一个[示例](https://github.com/huangwb8/m2w/blob/main/config/user.json)。根据实际情况修改参数即可。你可以创建很多个类似于`web01`的网站/帐户喔！参数解释如下：
+ **domain,username,password**：WordPress站点相关信息，比如站点URL、帐户名、密码。
+ **path_markdown**：添加任意多的顶级文件夹 (～￣▽￣)～ 
+ **post_metadata**：默认类别信息。有分类（category）、标签（tag）和状态（status）3个属性。
+ **websites**：可以添加任意数量的帐户 (～￣▽￣)～ 
+ **path_legacy_json**：不用改，保持原样。它是记录md5值用的，本质上是一个Python Dict的json版本。

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

4. 最后，运行脚本：

```bash
python '<path01>/m2w.py'
```

## 项目展示

如下图所示，只需要一行`python m2w.py`，即可自动更新或上传markdown喔！

![Code_Iscn3mHU78](https://chevereto.hwb0307.com/images/2022/12/11/Code_Iscn3mHU78.gif)

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

m2w项目采用MIT license。详见[LICENSE](https://github.com/huangwb8/m2w/blob/main/license.txt)。
