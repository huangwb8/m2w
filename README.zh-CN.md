# m2w: Markdown to WordPress

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
- [使用说明](#使用说明)
- [相关仓库](#相关仓库)
- [维护者](#维护者)
- [如何贡献](#如何贡献)
- [使用许可](#使用许可)

## 背景

`m2w` 是一个简单易用的自动上传和更新 markdown 到 WordPress 的工具，`m2w 1.0` 的开发工作已经在 `v1.0.7` 中被冻结。 `m2w 1.0` 对大多数人来说已经足够强大了，但有些特性对使用者不太友好：

+ 必须分配旧的或新的路径来存储博文，这意味着使用者无法随意放置文件。
+ 无法同时对多个站点进行管理。

你仍然可以找到m2w 1.0的使用说明（[中](https://github.com/huangwb8/m2w/blob/main/v1/README.zh-CN.md)/[英](https://github.com/huangwb8/m2w/blob/main/v1/README.md)），但我原则上不再维护`m2w 1.0`了。

现在，更强大的`m2w 2.0`来和大家见面啦！`m2w 2.0` 具有以下特点：

+ 与 `m2w 1.0` 相比，使用 和`config/user.json` 略微不同的方式维护用户信息。
+ 可以开心地保留原有的文件结构 (～￣▽￣)～ 。
+ 通过多个`legacy_*.json` 同时管理多个网站。
+ 只需要使用1个 python 脚本 `m2w.py` 而不是两个（`m2w 1.0` 中的 `update.py` 和 `upload.py`）。
+ 像m2w 1.0 稳定且好用！

## 安装使用

### 安装依赖：

```
pip3 install python-frontmatter
pip3 install markdown
pip3 install python-wordpress-xmlrpc
```

### 自定义user.json文件

+ **path_markdown**：添加任意多的顶级文件夹！
+ **post_metadata**：默认类别信息。
+ **websites**：添加任意数量的帐户！
+ **path_legacy_json**：不用管。

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

+ 下载整个项目。将脚本`m2w.py`的`path_m2w`参数改成你存放本仓库目录的绝对路径。比如我这个目录是放在`'E:/Github/m2w'`，可以设置：

  ```python
  path_m2w = 'E:/Github/m2w'
  ```

### 运行脚本

```bash
python3 <path>/m2w.py
```

## 项目展示

### 更新文章

![Code_gRt7iyCPOh](https://chevereto.hwb0307.com/images/2022/12/03/Code_gRt7iyCPOh.gif)

### 上传文章

![Code_FO6ElypOTt](https://chevereto.hwb0307.com/images/2022/12/03/Code_FO6ElypOTt.gif)

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

m2w项目采用MIT license。详见LICENSE。
