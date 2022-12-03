### [English](https://github.com/huangwb8/m2w) | [简体中文](https://github.com/huangwb8/m2w/blob/main/README.zh-CN.md)

# m2w: Markdown to WordPress

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
Automatically upload and update local markdown to WordPress via Python

Tutorial: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践](https://blognas.hwb0307.com/linux/docker/689)


## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Related Efforts](#related-efforts)
- [LOG](#LOG)
- [TO-DO](#TO-DO)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Demo

### Update

![Code_gRt7iyCPOh](https://chevereto.hwb0307.com/images/2022/12/03/Code_gRt7iyCPOh.gif)

### Upload

![Code_FO6ElypOTt](https://chevereto.hwb0307.com/images/2022/12/03/Code_FO6ElypOTt.gif)

## Background

`m2w` is an easy-to-use tool for automatical upload & update of  markdown to WordPress, which has been frozen in `v1.0.7`.  `m2w 1.0` is powerful enough for most people, but not very friendly: 

+ You have to assign `legacy` or `new` path to store the blog markdowns, which means that you could not position your files as you like.
+ It's not convenient to manage multiple sites with exactly the same blog markdowns.

Now, more powerful `m2w 2.0` comes and meet everyone! :star2: :star2: :star2:

`m2w 2.0` has these features: 

+ Use `config/user.json` to maintain the user information in a little different way comparing with `m2w 1.0`.
+ You can just keep your file structures locally as you like.
+ You can manage lots of websites at the same time via multiple `legacy_*.json`.
+ All you need to deal with is a single python script `m2w.py` instead of two (`update.py` and `upload.py` in `m2w 1.0`).
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
{
    "path_markdown": [
        "E:/Github/m2w/@test/main",
        "E:/Github/m2w/@test/main2"
    ],

    "post_metadata": {
        "category": ["test"],
        "tag": ["test"],
        "status": "publish"
    },

    "websites": {

        "web01": {
            "domain": "https://domain-01.com",
            "username": "user-01",
            "password": "password-01"
        },

        "web02": {
            "domain": "https://domain-02.com",
            "username": "user-02",
            "password": "password-02"
        }
    },

    "path_legacy_json": "/config/legacy"
}
```

### Define m2w.py

+ Download the Repo and save in `E:/Github/m2w`, for example. 

+ Set `path_m2w` as `'E:/Github/m2w'` in the script `m2w.py`, `get_posts.py`, and  `new_posts.py` .

  ```python
  path_m2w = 'E:/Github/m2w'
  ```

+ Scripts `get_posts.py` and `new_posts.py` are only used to test whether your `user.json` really work. In most application scenarios, `m2w.py` is the only one python script you need.

## Usage

+ Document tree:

```
blog
├──legacy
└──new
```

+ Write your new markdown in `new` document. Run `upload.py` to upload new markdowns.
+ Run `update.py` if any changes of markdowns appear in `legacy`document.

+ All scripts can be used as:

```bash
python3 <script>.py
```

Use demo with VScode: 

+ `upload.py`：

![image-20220424134824223](https://chevereto.hwb0307.com/images/2022/04/24/image-20220424134824223.png)

+  `update.py`：

![image-20220424125654213](https://chevereto.hwb0307.com/images/2022/04/24/image-20220424125654213.png)

## LOG

+ **2022-11-13**：Add error control for the `Client` function, which is helpful to avoid legacy bugs if the connection to the WordPress website is not available.
+ **Before**: Create `m2w` project.

## TO-DO

+ Less dependancy on the folder struction of markdowns.
+ Use WordPress API instead of username/password to upload/update new markdowns

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

Getting suggestions from [@nefu-ljw](https://github.com/nefu-ljw)

# More

+  [WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools)
