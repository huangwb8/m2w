### [English](https://github.com/huangwb8/m2w) | [简体中文](https://github.com/huangwb8/m2w/blob/main/README.zh-CN.md)

# m2w 2: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
Automatically upload and update local markdown to WordPress via Python

:star2::star2::star2: Welcome m2w 2!

Tutorial: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践-m2w 2.0](https://blognas.hwb0307.com/linux/docker/2813)


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

You can still find tutorials about m2w 1.0 ([ZH](https://github.com/huangwb8/m2w/blob/main/v1/README.zh-CN.md)/[En](https://github.com/huangwb8/m2w/blob/main/v1/README.md)), which is not maintained anymore. It's OK if you just use m2w 1.0, and It works very well.

\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=

Now, more powerful `m2w 2` comes and meet everyone! :star2: :star2: :star2:

`m2w 2` has these features: 

+ Use `config/user.json` to maintain the user information in a little different way comparing with `m2w 1.0`.
+ You can just keep your file structures locally as you like.
+ You can manage lots of websites at the same time via multiple `legacy_*.json`.
+ All you need to deal with is a single python script `m2w.py` instead of two (`update.py` and `upload.py` in `m2w 1.0`).
+ Ignore repeated new markdown files for uploading (`v2.2.4+`)
+ Stable and useful as `m2w 1.0`.

## Install

### Dependency

```
pip3 install python-frontmatter
pip3 install markdown
pip3 install python-wordpress-xmlrpc
```

### Define user.json

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

you can add many websites like `web01`! Please go [user.json](https://github.com/huangwb8/m2w/blob/main/config/user.json) for more details.

### Define m2w.py

+ Download the Repo and save in `E:/Github/m2w`, for example. 

+ Set `path_m2w` as `'E:/Github/m2w'` in the script `m2w.py`.

  ```python
  path_m2w = 'E:/Github/m2w'
  ```

### Usage

```bash
python3 <path>/m2w.py
```

## Demo

### Update

![Code_gRt7iyCPOh](https://chevereto.hwb0307.com/images/2022/12/03/Code_gRt7iyCPOh.gif)

### Upload

![Code_FO6ElypOTt](https://chevereto.hwb0307.com/images/2022/12/03/Code_FO6ElypOTt.gif)

## LOG

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

m2w is released under the MIT license. See [LICENSE](https://github.com/huangwb8/m2w/blob/main/license.txt) for details.

# More

> Applications similar to m2w

+  [WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools): Manage WordPress posts in Hexo way.
+  [markpress](https://github.com/skywind3000/markpress):  Write WordPress in Markdown in Your Favorite Text Editor
+  [wordpress-markdown-blog-loader](https://pypi.org/project/wordpress-markdown-blog-loader/): This utility loads markdown blogs into WordPress as a post. It allows you to work on your blog in your favorite editor and keeps all your blogs in git.
