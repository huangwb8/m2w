### [English](https://github.com/huangwb8/m2w) | [简体中文](https://github.com/huangwb8/m2w/blob/main/README.zh-CN.md)

# m2w 2: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w.svg?type=shield"/></a>
</p>
Automatically upload and update local markdown to WordPress via Python

:star2::star2::star2: Welcome m2w 2!

Tutorial: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)

Note (2023-02-23-): m2w v2.5 will support WordPress REST API but is still in beta version, which is not recommended. If m2w 2.5 was ready, we would release a stable version. Before that, [m2w v2.2.11](https://github.com/huangwb8/m2w/releases/tag/v2.2.11) is the best choice.


## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Demo](#demo)
- [Related Efforts](#related-efforts)
- [LOG](#LOG)
- [TO-DO](#TO-DO)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

`m2w` is an easy-to-use tool for automatical upload & update of markdown to WordPress, which has been frozen in `v1.0.7`.  `m2w 1.0` is powerful enough for most people, but not very friendly: 

+ You have to assign `legacy` or `new` path to store the blog markdowns, which means that you could not position your files as you like.
+ It's not convenient to manage multiple sites with exactly the same blog markdowns.

You can still find tutorials about m2w 1.0 ([Zh](https://github.com/huangwb8/m2w/blob/main/v1/README.zh-CN.md)/[En](https://github.com/huangwb8/m2w/blob/main/v1/README.md)), which is not maintained anymore. It's OK if you just use m2w 1.0, and It works very well.

\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=

Now, more powerful `m2w 2` comes and meet everyone! :star2: :star2: :star2:

`m2w 2` has these features: 

+ Use `config/user.json` to maintain the user information in a little different way comparing with `m2w 1.0`.
+ You can just keep your file structures locally as you like.
+ You can manage lots of websites at the same time via multiple `legacy_*.json`.
+ All you need to deal with is a single python script `myblog.py` instead of two (`update.py` and `upload.py` in `m2w 1.0`).
+ Ignore repeated new markdown files for uploading (`v2.2.4+`)
+ Stable and useful as `m2w 1.0`.

## Install

> [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is recommended to manage Python version and related dependencies.

Here is the dependency: 

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

After 2022-12-10, `m2w 2` was uploaded onto [PyPi](https://pypi.org/project/m2w/). To install `m2w 2`, just run `pip install m2w ` in your shell/conda environment. You can also directly download `m2w 2`  from this repotory. The usage is exactly the same.

You can specify version or resource when installing `m2w 2`:

```bash
pip install -i https://pypi.org/simple m2w==2.2.11
```

Generally, the latest version of `m2w` is recommended.

## Usage

1. Install m2w from PyPi or this Github repotory. 
2. Build a `myblog.py` file (or other names you like) in `<path01>`. Here is the [demo](https://github.com/huangwb8/m2w/blob/main/myblog.py). Create `<path02>/config/user.json` and set `path_m2w` as `<path02>` in `myblog.py`:

```python
# Absolute path of m2w
path_m2w = '<path02>'
```

3. Define `<path02>/config/user.json`.  You can add many websites like `web01`!  Please go to the [demo](https://github.com/huangwb8/m2w/blob/main/config/user.json) for more details. Here are some interpretations: 
  + **domain, username, password**:  The information of your WordPress site and account.
  + **path_markdown**: Add as much top folders as you want! 
  + **post_metadata**: Default category information. 
  + **websites**: Add as much accounts as you want! 
  + **path_legacy_json**: Just leave it alone and do not change anything!


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

4. Run `myblog.py` like: 

```bash
python <path01>/myblog.py
```

## Demo

> This demo is conducted in Win10 with [VScode](https://code.visualstudio.com/).

As shown in the following GIF, all changed or brand-new markdowns can be automatically updated/upload via just a simple command `python myblog.py`!

![Typora_zKwwaE10Qe](https://chevereto.hwb0307.com/images/2022/12/14/Typora_zKwwaE10Qe.gif)

## LOG

+ **2022-12-14** ：`m2w.py` is the same name as `m2w` package, which would bring some bugs. I change the name of the demo script as `myblog.py`.
+ **2022-12-10** ：Upload `m2w 2` to PyPi. You can install `m2w 2` with code (in Shell)  like `pip install -i https://pypi.org/simple m2w`. The project url is [https://pypi.org/project/m2w](https://pypi.org/project/m2w).
+ **2022-12-08** ：Ignore repeated uploading of new markdown based on their file names. Update ot `m2w 2.2.4` (Strongly recommended)! 
+ **2022-12-06**：Optimized parameter space of m2w, which make it more flexible. Update ot `m2w 2.2`!
+ **2022-12-03**：Brand-new m2w 2.0!
+ **2022-11-13**：Add error control for the `Client` function, which is helpful to avoid legacy bugs if the connection to the WordPress website is not available.
+ **Before**: Create `m2w` project.

## TO-DO

+ Nothing

## Related Efforts

- [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress)

## Maintainers

[@huangwb8](https://t.me/hwb0307)

## Contributing

Feel free to dive in! [Open an issue](https://github.com/huangwb8/m2w/issues/new) or submit PRs.

m2w follows the [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) Code of Conduct.

### Contributors

Nobody yet.


## License

This software depends on other packages that may be licensed under different open source licenses. 

m2w is released under the MIT license. See [LICENSE](https://github.com/huangwb8/m2w/blob/main/license.txt) for details.


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fhuangwb8%2Fm2w?ref=badge_large)

## More

> Applications similar to m2w

+  [WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools): Manage WordPress posts in Hexo way.
+  [markpress](https://github.com/skywind3000/markpress):  Write WordPress in Markdown in Your Favorite Text Editor
+  [wordpress-markdown-blog-loader](https://pypi.org/project/wordpress-markdown-blog-loader/): This utility loads markdown blogs into WordPress as a post. It allows you to work on your blog in your favorite editor and keeps all your blogs in git.