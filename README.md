### [English](README.md) | [简体中文](README.zh-CN.md)

# m2w: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w.svg?type=shield"/></a>
</p>
Automatically upload and update local markdown to WordPress based on REST API/Password via Python

:star2::star2::star2: Welcome m2w 2.5!

Chinese tutorial: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)


## Table of Contents

- [m2w: Markdown to WordPress](#m2w-markdown-to-wordpress)
  - [Table of Contents](#table-of-contents)
  - [Background](#background)
  - [Install](#install)
  - [Usage](#usage)
    - [Enable REST API](#enable-rest-api)
    - [Use m2w](#use-m2w)
  - [Demo](#demo)
  - [LOG](#log)
  - [TO-DO](#to-do)
  - [Related Efforts](#related-efforts)
  - [Maintainers](#maintainers)
  - [Contributing](#contributing)
  - [License](#license)
  - [More](#more)

## Background

`m2w` is a tool for automatically uploading or updating local Markdown to WordPress via Python, based on REST API (`2.5+`) or Password.

`m2w` has these features: 

+ **Support REST API**, which is safer then conventional password!
+ Use `config/user.json` to maintain the user information in a little different way comparing with `m2w 1.0`.
+ You can just keep your file structures locally as you like.
+ You can manage lots of websites at the same time via multiple `legacy_*.json`.
+ All you need to deal with is a single python script `myblog.py` instead of two (`update.py` and `upload.py` in `m2w 1.0`).
+ Ignore repeated new markdown files for uploading (`v2.2.4+`)

## Install

> [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is recommended to manage Python version and related dependencies.

Here is the dependency: 

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

After 2022-12-10, `m2w` was uploaded onto [PyPi](https://pypi.org/project/m2w/). To install `m2w`, just run this code in your shell/conda environment:

```
pip install m2w
```

You can also directly download `m2w`  from this repotory. The usage is exactly the same.

You can specify version or resource when installing `m2w`:

```bash
pip install -i https://pypi.org/simple m2w==2.5.13
```

Generally, the latest version of `m2w` is recommended.

## Usage

### Enable REST API

> This step is needed only **when you want to use the REST API mode**.

+ If any, please allow Application password of WordPress in Wordfence:

![WBrffVs5Ty](https://chevereto.hwb0307.com/images/2023/06/05/WBrffVs5Ty.png)

+ Go to personal settings and add a new REST API: 

![sq7kG7Vsqp](https://chevereto.hwb0307.com/images/2023/06/05/sq7kG7Vsqp.png)

+ Please record the new REST API in a safe place. If you forget it or suspect its safety, please remove the old API and create a new one:

![GddR0nP8mn](https://chevereto.hwb0307.com/images/2023/06/05/GddR0nP8mn.png)

### Use m2w

1. Install m2w from PyPi or this Github repotory. 
2. Build a `myblog.py` file (or other names you like) in `<path01>`. Here is the [demo](https://github.com/huangwb8/m2w/blob/main/myblog.py). Create `<path02>/config/user.json` and set `path_m2w` as `<path02>` in `myblog.py`:

```python
path_m2w = '<path02>' # Absolute path of m2w config folder
```

3. Define `<path02>/config/user.json`.  You can add many websites like `web01`!  Please go to the [demo](https://github.com/huangwb8/m2w/blob/main/config/user.json) for more details. Here are some interpretations: 
  + **user.json** for REST API mode:


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

+ **user.json** for Password mode: 


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

  + **domain, username, application_password/password**:  The information of your WordPress site and account. `application_password` is REST API, and `password` is the conventional passord of your account. if both `application_password` and `password` exit, only `application_password` is available for m2w.
  + **path_markdown**: Add as much top folders as you want! 
  + **post_metadata/path_legacy_json**: Set default if you don't know what they are. 

4. Run `myblog.py` like: 

```bash
python <path01>/myblog.py
```

## Demo

> This demo is conducted in Win10 with [VScode](https://code.visualstudio.com/).

As shown in the following GIF, all changed or brand-new markdowns can be automatically updated/upload via just a simple command `python myblog.py`!

![image-20230609173358533](https://chevereto.hwb0307.com/images/2023/06/09/image-20230609173358533.png)

## LOG

+ **2024-11-13**：Optimize optimize strategy for .md removement. [Detail](https://github.com/huangwb8/m2w/pull/18). Thanks [linglilongyi](https://github.com/linglilongyi)!
+ **2023-06-05**: m2w 2.0 was frozen at [v2.2.11](https://github.com/huangwb8/m2w/releases/tag/v2.2.11). Enjoy m2w 2.5+ from now on!
+ **2022-12-14**：`m2w.py` is the same name as `m2w` package, which would bring some bugs. I change the name of the demo script as `myblog.py`.
+ **2022-12-10**：Upload `m2w 2` to PyPi. You can install `m2w 2` with code (in Shell)  like `pip install -i https://pypi.org/simple m2w`. The project url is [https://pypi.org/project/m2w](https://pypi.org/project/m2w).
+ **2022-12-08**：Ignore repeated uploading of new markdown based on their file names. Update ot `m2w 2.2.4` (Strongly recommended)! 
+ **2022-12-06**：Optimized parameter space of m2w, which make it more flexible. Update ot `m2w 2.2`!
+ **2022-12-03**：Brand-new m2w 2.0!
+ **2022-11-13**：Add error control for the `Client` function, which is helpful to avoid legacy bugs if the connection to the WordPress website is not available.
+ **Before**: Create `m2w` project.

## TO-DO

- [ ] shuoshuo and page update & upload

- [ ] Enhanced markdown support: `python-markdown` to `markdown-it-py`

- [ ] Support Hexo-like YAML head：

```yaml
title: I Love You
tags:
  - You
  - I
  - Love
categories:
  - Note
date: 2023-11-08 16:38:31
update: 2023-11-08 16:40:31
--
```

- [ ] Develop GUI across OS

## Related Efforts

- [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)

## Maintainers

+ [@huangwb8](https://t.me/hwb0307)

## Contributing

> Feel free to dive in! [Open an issue](https://github.com/huangwb8/m2w/issues/new) or submit PRs. m2w follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

<a href="https://github.com/huangwb8/m2w/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=huangwb8/m2w" />
</a>

## License

This software depends on other packages that may be licensed under different open source licenses. 

m2w is released under the MIT license. See [LICENSE](https://github.com/huangwb8/m2w/blob/main/license.txt) for details.


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w?ref=badge_large)

## More

> Applications similar to m2w

+  [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress): The root project of m2w!
+  [WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools): Manage WordPress posts in Hexo way.
+  [markpress](https://github.com/skywind3000/markpress):  Write WordPress in Markdown in Your Favorite Text Editor
+  [wordpress-markdown-blog-loader](https://pypi.org/project/wordpress-markdown-blog-loader/): This utility loads markdown blogs into WordPress as a post. It allows you to work on your blog in your favorite editor and keeps all your blogs in git.
