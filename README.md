### [English](https://github.com/huangwb8/m2w) | [简体中文](https://github.com/huangwb8/m2w/blob/main/README.zh-CN.md)

# m2w: Markdown to WordPress

> :star2: :star2: :star2: Later, m2w 2.0 will meet everyone! More humanized design and compatible with your local markdown structure!

<p align="left">
<a href=""><img src="https://img.shields.io/badge/python-3.7%2B-orange"></a>
<a href=""><img src="https://img.shields.io/badge/platform-Windows%7Clinux%7CMacOS-brightgreen"></a>
<a href=""><img src="https://img.shields.io/github/downloads/huangwb8/m2w/total"></a>
<a href=""><img src="https://img.shields.io/github/stars/huangwb8/m2w?style=social"></a>
</p>
Automatically upload and update local markdown to WordPress via Python

Demo: [https://blognas.hwb0307.com](https://blognas.hwb0307.com)

Tutorial: [Docker系列 WordPress系列 WordPress上传或更新Markdown的最佳实践](https://blognas.hwb0307.com/linux/docker/689)

![](https://chevereto.hwb0307.com/images/2022/05/27/Code_6OcltCZ2le.gif)


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

## Background

> Recently, [WordPressXMLRPCTools](https://github.com/zhaoolee/WordPressXMLRPCTools) has been recommanded as an alternative platform for the WordPress blog management, which is based on Github Actions similar to Hexo. Thanks for jobs from [cye](https://github.com/cye18)!

Recently I started to play WordPress blog. I've use [Typora](https://github.com/typora) for nearly 2 years, so I hope I can edit my blogs locally via [Typora](https://github.com/typora). Also, the content of some old blogs might change, and I don't want to update them step by step with WordPress dashboard. So, I just looked for **an easy-to-use tool for automatical upload & update of  markdown** with minimum operation in WordPress dashboard. 

Finally, I found the project [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress) available for this need. However, this project does not possess enough automation in updating old markdowns. It is also necessary for users to repeatedly declare exactly the same private information among scripts. 

`m2w` is based on [nefu-ljw/python-markdown-to-wordpress](https://github.com/nefu-ljw/python-markdown-to-wordpress) and has some new features：

+ Use `config/user.json` to maintain the user information
+ File management via `new`和`legacy` documents
+ The md5 sum of files in the `legacy` document would be calculated before updating. Only files with changes would be update. New md5 sum of legacy markdowns would be stored in the `config/legacy.json` file.

## Install

+ Dependency

```
pip3 install python-frontmatter
pip3 install markdown
pip3 install python-wordpress-xmlrpc
```

+ Define your `config/user.json`

```json
{
    // Main 
    "main": "E:/Github/m2w/blog",
    
    // Main/new
    "symbol_new": "new",
    
    // Main/legacy
    "symbol_legacy": "legacy",
    
    // Domain, Username, and Password
    "domain": "https://blog.domain.com",
    "username": "user",
    "password": "user_password",
    
    // Default category, tag or status of articles
    "post_metadata": {
        "category": ["test"],
        "tag": ["test"],
        "status": "publish"
    },
    
    // Do not change this setting
    "path_legacy_json": "/config/legacy.json"
}
```

+ Download the Repo and save in `E:/Github/m2w`, for example. Set `path_m2w` as `'E:/Github/m2w'` in every script.

  ```python
  path_m2w = 'E:/Github/m2w'
  ```

+ Scripts `get_posts.py` and `new_posts.py` are only used to test whether your `user.json` really work.

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
